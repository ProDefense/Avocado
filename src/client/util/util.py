import os
import pathlib
import urllib.parse
from typing import Tuple

def parseEndpoint(endpoint: str) -> Tuple[str, int]:
    result = urllib.parse.urlsplit(f"//{endpoint}")
    if result.hostname is None:
        raise ValueError(f"Invalid hostname in endpoint {endpoint}")

    if result.port is None:
        raise ValueError(f"Invalid port in endpoint {endpoint}")

    return result.hostname, result.port

def _get_avocado_root():
    # Check for AVOCADO_ROOT env variable
    avocado_root = os.environ.get("AVOCADO_ROOT")
    if avocado_root is not None:
        return avocado_root

    # Set to $HOME/.avocado
    avocado_root = pathlib.Path.home()
    if avocado_root is not None:
        return os.path.join(avocado_root, ".avocado")

    # Set to $PWD/.avocado
    return os.path.join(os.getcwd(), ".avocado")


def _init_avocado_root():
    avocado_root = _get_avocado_root()
    try:
        os.mkdir(avocado_root, mode=0o750)
    except FileExistsError:
        pass
    return avocado_root


AVOCADO_ROOT = _init_avocado_root()
