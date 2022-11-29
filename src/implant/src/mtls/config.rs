use anyhow::{anyhow, Result};
use crate::embed::Assets;
use std::io::BufReader;

/// Client configurations for mutual TLS
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

/// Load the server's root CA certificate
fn load_root_store(root_ca: &str) -> Result<rustls::RootCertStore> {
    let root_ca = Assets::get(root_ca)
        .ok_or_else(|| anyhow!("{} not found in Assets", root_ca))?;

    let mut capath = BufReader::new(root_ca.data.as_ref());
    let mut root_store = rustls::RootCertStore::empty();
    root_store.add_parsable_certificates(&rustls_pemfile::certs(&mut capath)?);
    Ok(root_store)
}

/// Load the client pem certificate
fn load_pem(client_pem: &str) -> Result<Vec<rustls::Certificate>> {
    let client_pem = Assets::get(client_pem)
        .ok_or_else(|| anyhow!("{} not found in Assets", client_pem))?;

    let mut client_pem = BufReader::new(client_pem.data.as_ref());
    Ok(rustls_pemfile::certs(&mut client_pem)?
     .iter()
     .map(|v| rustls::Certificate(v.clone()))
     .collect())
}

/// Load the client's private key
fn load_key(client_key: &str) -> Result<rustls::PrivateKey> {
    let client_key = Assets::get(client_key)
        .ok_or_else(|| anyhow!("{} not found in Assets", client_key))?;

    let mut client_key = BufReader::new(client_key.data.as_ref());
    match rustls_pemfile::read_one(&mut client_key)? {
        Some(rustls_pemfile::Item::PKCS8Key(key)) => Ok(rustls::PrivateKey(key)),
        _ => Err(anyhow!("Invalid key")),
    }
}
