FROM archlinux

# WARNING: This docker file is used for testing only.

RUN \
  pacman -Sy base-devel rustup python python-pip protobuf mkcert mingw-w64-gcc --noconfirm && \
  useradd -M avocado

COPY . /home/avocado
RUN chown -R avocado:avocado /home/avocado
WORKDIR /home/avocado
USER avocado

RUN \
  pip install -r requirements.txt && \
  rustup default nightly && \
  rustup target add x86_64-unknown-linux-musl && \
  rustup target add x86_64-pc-windows-gnu && \
  cargo check --release --target=x86_64-pc-windows-gnu --manifest-path=$HOME/src/implant/Cargo.toml || echo "checked windows" && \
  cargo check --release --target=x86_64-unknown-linux-musl --manifest-path=$HOME/src/implant/Cargo.toml || echo "checked linux" && \
  echo "alias ls='ls --color'" >> $HOME/.bashrc

CMD [ "/bin/bash" ]
