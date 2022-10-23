use anyhow::Result;
use crate::pb::{User, Registration};

// TODO: write registration for Windows. This is for Linux only
pub fn register() -> Result<Registration> {
    Ok(Registration { 
        ip: ip()?,
        os: os()?,
        pid: pid()?,
        user: Some(user()?),
        groups: groups()?
    })
}

// Get the current operating system name by parsing /etc/os-release
fn os() -> Result<String> {
    Ok(String::from("TODO"))
}

// Get the IP address on the interface that connects back to the C2 server
fn ip() -> Result<String> {
    Ok(String::from("TODO"))
}

// Get the current process id of the running implant
fn pid() -> Result<u32> {
    Ok(0)
}

// Get the user running the implant
fn user() -> Result<User> {
    let u = User {
        id: 0,
        name: String::from("TODO")
    };
    Ok(u)
}

// Get the groups this user is a part of
fn groups() -> Result<Vec<User>> {
    let g = User {
        id: 0,
        name: String::from("TODO")
    };
    Ok(vec![g])
}
