FROM archlinux

# WARNING: This docker file is used for testing only.
# For an actual deployment, see the installation guide in the README

RUN \
  pacman -Syu --noconfirm && \
  pacman -S base-devel rustup python python-pip protobuf mkcert --noconfirm && \
  useradd -M avocado

COPY . /home/avocado
RUN chown -R avocado:avocado /home/avocado
WORKDIR /home/avocado
USER avocado

RUN \
  pip install -r requirements.txt && \
  # rustup install x86_64-unknown-linux-musl && \
  rustup target add x86_64-pc-windows-msvc

CMD [ "/bin/bash" ]
