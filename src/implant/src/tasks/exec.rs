use std::process::{Command, Output};

/// Executes a command and returns the result
#[cfg(target_os = "linux")]
pub fn exec(cmd: &str) -> anyhow::Result<Output> {
    let cmd = cmd.trim_matches(char::from(0));
    let output = Command::new("/bin/bash").args(["-c", cmd]).output()?;
    Ok(output)
}

#[cfg(target_os = "windows")]
pub fn exec(cmd: &str) -> anyhow::Result<Output> {
    let cmd = cmd.trim_matches(char::from(0));
    let output = Command::new("cmd").args(["/C", cmd]).output()?;
    Ok(output)
}
