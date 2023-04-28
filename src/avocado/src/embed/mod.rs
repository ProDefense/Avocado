//! Embedded files, certificates, and other compile-time constants
use rust_embed::RustEmbed;

/// The endpoint address of the C2 server, such as 172.17.0.2:31337
pub const SERVER_ENDPOINT: &'static str = env!("SERVER_ENDPOINT");

/// The domain name associated with the server's x509 certificate
pub const SERVER_NAME: &'static str = env!("SERVER_NAME");

/// The basename of the server's rootca.
pub const SERVER_ROOTCA: &'static str = env!("SERVER_ROOTCA");

/// The basename of this implant's private key
pub const IMPLANT_PRIVATE_KEY: &'static str = env!("IMPLANT_PRIVATE_KEY");

/// The basename of this implant's public key
pub const IMPLANT_PUBLIC_KEY: &'static str = env!("IMPLANT_PUBLIC_KEY");

#[derive(RustEmbed)]
#[folder = "$IMPLANT_ASSETS_DIR/"]
pub struct Assets;
