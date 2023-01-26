# Compile the implant
import os
import subprocess
from certs.certs import Certs
from util.util import AVOCADO_ROOT


# Create a profile to generate an implant.
class Profile:
    def __init__(
            self,
            server_endpoint: str,
            implant_certs: Certs,
            out_dir: str,
            assets_dir: str,
            target_os: str,
            server_name: str = "server",
            server_rootca: str = "rootCA.pem"):
        self.server_endpoint = server_endpoint  # Server url
        self.server_name = server_name  # Server x509 name
        self.server_rootca = server_rootca  # Name of the server rootca cert
        self.implant_certs = implant_certs  # Implant certificats
        self.assets_dir = assets_dir  # Embed files into the implant
        self.target_os = target_os  # Either "linux" or "windows"
        self.out_dir = out_dir  # Which directory to output the implant binary

    # Run cargo build.
    def generate(self):
        exit_code = self._cargo_build(os.path.join("..", "implant", "Cargo.toml"))
        if exit_code != 0 and exit_code != 1:
            exit_code = self._cargo_build(os.path.join(AVOCADO_ROOT, "implant", "Cargo.toml"))
        if exit_code != 0 and exit_code != 1:
            print(f"Subprocess error: cargo build failed with exit code {exit_code}")

    def _cargo_build(self, cargo_toml_path: str) -> int:
        path = os.environ["PATH"]
        args = ["/usr/bin/cargo", "build", "-Z", "unstable-options", "--manifest-path", cargo_toml_path, "--out-dir", self.out_dir, "--release"]
        if self.target_os == "linux":
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
                "IMPLANT_PRIVATE_KEY": os.path.basename(self.implant_certs.private_key),
                "IMPLANT_PUBLIC_KEY": os.path.basename(self.implant_certs.public_key),
                "IMPLANT_ASSETS_DIR": self.assets_dir
            },
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        ).wait()
        return exit_code


# A wrapper for the generate command
def generate(implant_certs: Certs, target_os: str) -> Profile:
    # Create a directory to store implant assets
    assets_dir = os.path.join(AVOCADO_ROOT, "implant_assets")
    try:
        os.makedirs(assets_dir, mode=0o750)
    except FileExistsError:
        pass

    # Symlink the certs into the assets directory
    try:
        os.symlink(implant_certs.private_key, os.path.join(assets_dir, os.path.basename(implant_certs.private_key)))
        os.symlink(implant_certs.public_key, os.path.join(assets_dir, os.path.basename(implant_certs.public_key)))
        os.symlink(os.path.join(AVOCADO_ROOT, "certs", "server", "rootCA.pem"), os.path.join(assets_dir, "rootCA.pem"))
    except FileExistsError:
        pass

    # Compile the implant.
    profile = Profile(
        server_endpoint="127.0.0.1:31337",
        implant_certs=implant_certs,
        out_dir=".",
        assets_dir=assets_dir,
        target_os=target_os
    )
    profile.generate()
    return profile
