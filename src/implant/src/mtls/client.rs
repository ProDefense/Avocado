// use std::{net::TcpStream, sync::Arc, io::{Write, Read}};
use std::net::TcpStream;
use std::sync::Arc;
use std::io::{Read, Write};
use anyhow::{Result, Ok};
use prost::Message;
use rustls::{ClientConfig, ClientConnection, Stream};

use super::Server;
use crate::tasks::registration::register;

pub struct Client {
    conn: ClientConnection,
    sock: TcpStream
}

impl Client {
    pub fn new(config: ClientConfig, server :Server) -> Result<Client> {
        // Connect to the server
        let conn = ClientConnection::new(Arc::new(config), server.name)?;
        let sock = TcpStream::connect(server.addr)?;

        // TODO: Register with the server
        let mut client = Client {
            conn,
            sock
        };

        client.write(register()?.encode_to_vec())?;
        Ok(client)
    }

    /// Read 1024 bytes from the tls stream
    /// BUG: For some reason this keeps receiving data even when the connection is closed.
    pub fn read(&mut self) -> Result<String> {
        let mut tls = Stream::new(&mut self.conn, &mut self.sock);
        let mut buffer = [0; 1024];
        tls.read(&mut buffer[..]).unwrap();
        let s = std::str::from_utf8(&buffer)?
            .to_string();
        Ok(s)
    }

    /// TODO: Don't make a new stream each time.
    pub fn write(&mut self, buf: Vec<u8>) -> Result<()> {
        let mut tls = Stream::new(&mut self.conn, &mut self.sock);
        tls.write(&buf)?;
        Ok(())
    }
}
