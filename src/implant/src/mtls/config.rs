use anyhow::{anyhow, Result};
use std::fs::File;
use std::io::BufReader;

pub fn client_config(
    root_ca: &str,
    client_pem: &str,
    client_key: &str,
) -> Result<rustls::ClientConfig> {
    let root_store = load_root_store(root_ca)?;
    let client_pem = load_pem(client_pem)?;
    let client_key = load_key(client_key)?;

    let mut config = rustls::ClientConfig::builder()
        .with_safe_defaults()
        .with_root_certificates(root_store)
        .with_single_cert(client_pem, client_key)?;

    config.alpn_protocols = vec!["PostHandshakeAuth".as_bytes().to_vec()];
    Ok(config)
}

/// Load the server's CA cert
fn load_root_store(capath: &str) -> Result<rustls::RootCertStore> {
    let mut capath = BufReader::new(File::open(capath)?);
    let mut root_store = rustls::RootCertStore::empty();
    root_store.add_parsable_certificates(&rustls_pemfile::certs(&mut capath)?);
    Ok(root_store)
}

/// Load the client pem certificate
fn load_pem(client_pem: &str) -> Result<Vec<rustls::Certificate>> {
    let mut client_pem = BufReader::new(File::open(client_pem)?);
    let pem = rustls_pemfile::certs(&mut client_pem)?
        .iter()
        .map(|v| rustls::Certificate(v.clone()))
        .collect();
    Ok(pem)
}

/// Load the client's private key
fn load_key(client_key: &str) -> Result<rustls::PrivateKey> {
    let mut client_key = BufReader::new(File::open(client_key)?);
    match rustls_pemfile::read_one(&mut client_key)? {
        Some(rustls_pemfile::Item::PKCS8Key(key)) => Ok(rustls::PrivateKey(key)),
        _ => Err(anyhow!("Invalid key")),
    }
}
