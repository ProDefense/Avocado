use std::process::{Command, Output};

/// Only for linux
/// Executes a command and returns the result
/// BUG: For some reason, null bytes in the `cmd` parameter will break this.
pub fn exec(cmd: &str) -> anyhow::Result<Output> {
    let cmd = cmd.trim_matches(char::from(0));
    let output = Command::new("/bin/bash").args(["-c", cmd]).output()?;
    Ok(output)
}
