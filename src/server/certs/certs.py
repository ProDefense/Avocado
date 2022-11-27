# This is a dumb script to run `mkcert` until I
# can figure out how to make x509 work in python.
# https://github.com/FiloSottile/mkcert
# The SSL python package doesn't like the x509 certs that
# come out of the `pyca/cryptography` package :(

import os
import subprocess
from util.util import AVOCADO_ROOT


class Certs:
    def __init__(self, name):
        self.name = name
        self.dir, self.public_key, self.private_key = self._mkcert()
        self.rootCA = os.path.join(self.dir, "rootCA.pem")

    def _mkcert(self):
        cert_dir = os.path.join(AVOCADO_ROOT, "certs", self.name)
        public_key = os.path.join(cert_dir, f"{self.name}.pem")
        private_key = os.path.join(cert_dir, f"{self.name}-key.pem")
        try:
            os.makedirs(cert_dir, mode=0o750)
        except FileExistsError:
            pass

        # Run the `mkcert command`
        subprocess.Popen(
            ["mkcert", "-ecdsa", "-cert-file", public_key, "-key-file", private_key, self.name],
            env={"CAROOT": cert_dir},
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return cert_dir, public_key, private_key
