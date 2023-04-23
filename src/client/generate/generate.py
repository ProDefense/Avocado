# Compile the implant
import os
import subprocess
from client.certs.certs import cert_generator
from client.util.util import AVOCADO_ROOT


# Create a profile to generate an implant.
class Profile:
    def __init__(
            self,
            server_endpoint: str,
            implant_certs: (str, str),
            out_dir: str,
            assets_dir: str,
            target_os: str,
            server_name: str = "server",
            server_rootca: str = "root.pem"):
        self.server_endpoint = server_endpoint  # Server url
        self.server_name = server_name  # Server x509 name
        self.server_rootca = server_rootca  # Name of the server rootca cert
        self.implant_certs = implant_certs  # Implant certificate locations in relation to AVOCADO_ROOT
        self.assets_dir = assets_dir  # Embed files into the implant
        self.target_os = target_os  # Either "linux" or "windows"
        self.out_dir = out_dir  # Which directory to output the implant binary

    # Run cargo build.
    def generate(self):
        exit_code = self._cargo_build(os.path.join("avocado", "Cargo.toml"))
        if exit_code != 0 and exit_code != 1:
            exit_code = self._cargo_build(os.path.join(AVOCADO_ROOT, "implant", "Cargo.toml"))
        if exit_code != 0 and exit_code != 1:
            print(f"Subprocess error: cargo build failed with exit code {exit_code}")

    def _cargo_clean(self, cargo_toml_path: str) -> int:
        args = ["/usr/bin/cargo", "clean", "--manifest-path", cargo_toml_path]
        exit_code = subprocess.Popen(
            args,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        ).wait()
        return exit_code

    def _cargo_build(self, cargo_toml_path: str) -> int:
        self._cargo_clean(cargo_toml_path)
        path = os.environ["PATH"]
        args = ["cargo", "build", "-Z", "unstable-options", "--manifest-path", cargo_toml_path, "--out-dir", self.out_dir, "--release"]
        if self.target_os == "linux":
            args.extend(["-Z", "build-std=std,panic_abort",])
            args.extend(["-Z", "build-std-features=panic_immediate_abort"])
            args.append("--target=x86_64-unknown-linux-musl")
        elif self.target_os == "windows":
            args.append("--target=x86_64-pc-windows-gnu")

        exit_code = subprocess.Popen(
            args,
            env={
                "PATH": path,
                "SERVER_ENDPOINT": self.server_endpoint,
                "SERVER_NAME": self.server_name,
                "SERVER_ROOTCA": os.path.basename(self.server_rootca),
                "IMPLANT_PRIVATE_KEY": os.path.basename(self.implant_certs[1]),
                "IMPLANT_PUBLIC_KEY": os.path.basename(self.implant_certs[0]),
                "IMPLANT_ASSETS_DIR": self.assets_dir
            },
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        ).wait()
        return exit_code


# A wrapper for the generate command
def generate(endpoint: str, target_os: str) -> Profile:
    # Create a directory to store implant assets
    assets_dir = os.path.join(AVOCADO_ROOT, "implant_assets")
    try:
        os.makedirs(assets_dir, mode=0o750)
    except FileExistsError:
        pass

    # Symlink the certs into the assets directory
    try:
        implant_certgen = cert_generator('implant', client=True)
        cert_path, key_path = implant_certgen.build_x509_cert()

        os.symlink(cert_path, os.path.join(assets_dir, os.path.basename(cert_path)))
        os.symlink(key_path, os.path.join(assets_dir, os.path.basename(key_path)))
        os.symlink(os.path.join(AVOCADO_ROOT, "certs", "root", "root.pem"), os.path.join(assets_dir, "root.pem"))
    except FileExistsError:
        pass

    # Compile the implant.
    profile = Profile(
        server_endpoint=endpoint,
        implant_certs=(cert_path, key_path),
        out_dir=".",
        assets_dir=assets_dir,
        target_os=target_os
    )
    profile.generate()
    return profile
