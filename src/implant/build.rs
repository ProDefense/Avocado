fn main() {
    prost_build::compile_protos(&["src/implantpb.proto"], &["src/"]).unwrap();
}
