"""
In interactive cli shell for Avocado
"""
import click
from click_shell import shell

import uuid
from mtls import mtls
from compile import compile

pass_listener = click.make_pass_decorator(mtls.Listener)


@shell(prompt="avocado-server > ", intro="Starting Avocado Server...", hist_file=".avocado_history")
@click.pass_context
def console(ctx):
    ctx.ensure_object(mtls.Listener)


@console.command()
@pass_listener
def sessions(listener: mtls.Listener):
    for id in listener.sessions.list():
        print(id)


@console.command()
@click.option("-i", "--id", "id", type=click.UUID, required=True)
@pass_listener
def use(listener: mtls.Listener, id: uuid.UUID):
    conn, addr = listener.sessions.get(id)
    print(f"Using session with {addr}")
    mtls.session(conn)


@console.command()
@click.option("-e", "--endpoint", "endpoint", type=click.STRING, required=True)
@click.option("-p", "--platform", "platform", type=click.Choice(["linux", "windows"]), required=True)
@pass_listener
def generate(listener: mtls.Listener, endpoint: str, platform: str):
    print("Generating the implant...")
    compile.generate(listener.client_certs, endpoint, platform)
