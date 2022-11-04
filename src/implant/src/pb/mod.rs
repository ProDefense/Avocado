mod implantpb {
    include!(concat!(env!("OUT_DIR"), "/implantpb.rs"));
}

pub use implantpb::*;
