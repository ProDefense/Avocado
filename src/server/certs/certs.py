# This is a dumb script to run `mkcert` until I
# can figure out how to make x509 work in python.
# https://github.com/FiloSottile/mkcert
# The SSL python package doesn't like the x509 certs that
# come out of the `pyca/cryptography` package :(

import os
import subprocess
from util.util import AVOCADO_ROOT


# Make x509 certificates and store them in $AVOCADO_ROOT/certs/{name}
class Certs:
    def __init__(self, name: str, client: bool):
        # Domain name associated with the x509 cert
        self.name = name
        self.is_client = client
        # Get the directory of the files, the pathname public key, and the pathname of the private key
        cert_dir, public_key, private_key = self._mkcert()
        self.cert_dir = cert_dir
        self.public_key = public_key
        self.private_key = private_key
        self.rootCA = os.path.join(self.cert_dir, "rootCA.pem")

    def _mkcert(self):
        cert_dir = os.path.join(AVOCADO_ROOT, "certs", self.name)
        public_key = os.path.join(cert_dir, f"{self.name}.pem")
        private_key = os.path.join(cert_dir, f"{self.name}-key.pem")
        try:
            os.makedirs(cert_dir, mode=0o750)
        except FileExistsError:
            pass

        if self.is_client:
            args = ["/usr/bin/mkcert", "-ecdsa", "-client", "-cert-file", public_key, "-key-file", private_key, self.name]
        else:
            args = ["/usr/bin/mkcert", "-ecdsa", "-cert-file", public_key, "-key-file", private_key, self.name]

        # Run the `mkcert command`
        exit_code = subprocess.Popen(
            args,
            env={"CAROOT": cert_dir},
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        ).wait()
        if exit_code != 0:
            print(f"Subprocess Error: mkcert failed with exit code {exit_code}")

        return cert_dir, public_key, private_key
