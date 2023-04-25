FROM postgres

# WARNING: This docker file is used for testing only.

#USER root

RUN \
  # Just Debian things
  apt update && \
  apt install curl build-essential binutils-mingw-w64 mingw-w64 python3 python3-pip musl musl-dev musl-tools protobuf-compiler postgresql-contrib -y && \
  ln -s /usr/bin/python3 /usr/local/bin/python && \
  # Install mkcert
  curl -JL "https://dl.filippo.io/mkcert/latest?for=linux/amd64" -o /usr/bin/mkcert && \
  chmod +x /usr/bin/mkcert
  #chmod +x /usr/bin/mkcert && \
  #useradd -M avocado

COPY . /root
#RUN chown -R avocado:avocado /root
WORKDIR /root
#USER avocado

ENV POSTGRES_PASSWORD password
ENV POSTGRES_DB test_db
COPY avocado.sql /docker-entrypoint-initdb.d/

#USER root

#EXPOSE 5432

ENV PATH="/root/.cargo/bin:${PATH}"

RUN \
  # Install python packages
  pip install -r requirements.txt && \
  # Install rustup
  bash -c "curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y" && \
  # Install toolchains
  rustup default nightly && \
  rustup target add x86_64-unknown-linux-musl && \
  rustup target add x86_64-pc-windows-gnu && \
  rustup component add rust-src --toolchain nightly-x86_64-unknown-linux-gnu && \
  # Cache things needed to compile the implant
  cargo check --release --target=x86_64-pc-windows-gnu --manifest-path=$HOME/src/implant/Cargo.toml || echo "checked windows" && \
  cargo check --release --target=x86_64-unknown-linux-musl --manifest-path=$HOME/src/implant/Cargo.toml || echo "checked linux" && \
  echo "alias ls='ls --color'" >> $HOME/.bashrc && \
  echo 'export PATH=$HOME/.cargo/bin:$PATH' >> $HOME/.bashrc
  #ln -s /root/.cargo/bin/cargo /usr/bin/cargo


#USER avocado
#CMD [ "/bin/bash" ]