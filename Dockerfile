FROM --platform=linux/amd64 archlinux

# WARNING: This docker file is used for testing only.
# For an actual deployment, see the installation guide in the README

RUN pacman -Syu --noconfirm && \
    pacman -S base-devel rust python python-pip protobuf mkcert --noconfirm && \
    useradd -M avocado

# Running an ubuntu docker container
#FROM --platform=linux/amd64 ubuntu:latest
#
#RUN apt-get update && \
#    apt-get install -y protobuf-compiler && \
#    curl --proto '=https' --tisv1.2 https://sh.rustup.rs -sSf | sh && \
#    apt-get install -y python3.10 python3-pip && \
#    apt-get install -y mkcert && \
#    useradd -M avocado
#
#RUN pip install --upgrade pip && pip install PyQt6-sip==13.4.0

# End of ubuntu docker container install instructions

COPY . /home/avocado
RUN chown -R avocado:avocado /home/avocado
WORKDIR /home/avocado
USER avocado

RUN pip install -r requirements.txt

CMD [ "/bin/bash" ]
