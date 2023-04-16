FROM --platform=linux/amd64 archlinux

# WARNING: This docker file is used for testing only.

RUN \
  pacman -Sy base-devel rustup python python-pip protobuf mingw-w64-gcc musl --noconfirm && \
  useradd -M avocado

# Running an ubuntu docker container
#FROM --platform=linux/amd64 ubuntu:latest
#
#RUN apt-get update && \
#    apt-get install -y protobuf-compiler && \
#    curl --proto '=https' --tisv1.2 https://sh.rustup.rs -sSf | sh && \
#    apt-get install -y python3.10 python3-pip && \
#    useradd -M avocado
#
#RUN pip install --upgrade pip && pip install PyQt6-sip==13.4.0

# End of ubuntu docker container install instructions

COPY . /home/avocado
RUN chown -R avocado:avocado /home/avocado
WORKDIR /home/avocado
USER avocado

RUN \
  pip install -r requirements.txt && \
  rustup default nightly && \
  rustup target add x86_64-unknown-linux-musl && \
  rustup target add x86_64-pc-windows-gnu && \
  rustup component add rust-src --toolchain nightly-x86_64-unknown-linux-gnu && \
  cargo check --release --target=x86_64-pc-windows-gnu --manifest-path=$HOME/src/implant/Cargo.toml || echo "checked windows" && \
  cargo check --release --target=x86_64-unknown-linux-musl --manifest-path=$HOME/src/implant/Cargo.toml || echo "checked linux" && \
  echo "alias ls='ls --color'" >> $HOME/.bashrc

CMD [ "/bin/bash" ]
