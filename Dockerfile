FROM archlinux

# WARNING: This docker file is used for testing only.
# For an actual deployment, see the installation guide in the README

RUN pacman -Syu --noconfirm && \
    pacman -S base-devel rust python python-pip protobuf mkcert --noconfirm && \
    useradd -M avocado

COPY . /home/avocado
RUN chown -R avocado:avocado /home/avocado
WORKDIR /home/avocado
USER avocado
RUN pip install -r requirements.txt

CMD [ "/bin/bash" ]
