use std::convert::TryFrom;

use anyhow::Result;
use std::net::SocketAddr;

pub struct Server {
    pub addr: SocketAddr,
    pub name: rustls::ServerName,
}

impl Server {
    pub fn new(addr: SocketAddr, hostname: &str) -> Result<Server> {
        Ok(Server {
            addr,
            name: rustls::ServerName::try_from(hostname)?,
        })
    }
}
