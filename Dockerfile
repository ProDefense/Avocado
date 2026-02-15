FROM --platform=linux/amd64 ubuntu:24.04

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    gcc-mingw-w64-x86-64 \
    g++-mingw-w64-x86-64 \
    libffi-dev \
    musl-tools \
    protobuf-compiler \
    python3 \
    python3-dev \
    python3-pip \
    && useradd -M avocado \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp/requirements.txt
RUN pip3 install --break-system-packages -r /tmp/requirements.txt && rm /tmp/requirements.txt

COPY . /home/avocado
RUN chown -R avocado:avocado /home/avocado && chmod +x /home/avocado/entrypoint.sh

WORKDIR /home/avocado
USER avocado
ENV PATH="/home/avocado/.cargo/bin:${PATH}"
ENTRYPOINT ["/home/avocado/entrypoint.sh"]

RUN curl -sSf https://sh.rustup.rs | sh -s -- -y --default-toolchain none \
    && . "$HOME/.cargo/env" \
    && rustup default nightly \
    && rustup target add x86_64-unknown-linux-musl x86_64-pc-windows-gnu \
    && rustup component add rust-src --toolchain nightly-x86_64-unknown-linux-gnu

CMD ["server"]
