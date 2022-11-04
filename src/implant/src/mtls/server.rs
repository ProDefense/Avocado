use std::convert::TryFrom;

use anyhow::Result;

pub struct Server {
    pub addr: String,
    pub name: rustls::ServerName,
}

impl Server {
    pub fn new(addr: String, hostname: &str) -> Result<Server> {
        Ok(Server {
            addr,
            name: rustls::ServerName::try_from(hostname)?,
        })
    }
}
