FROM python:3.9-slim

RUN apt-get update && apt-get install -y apt-transport-https \
    ca-certificates \
    build-essential \
    software-properties-common \
    libpq-dev \
    python3-dev \
    curl \
    postgresql \
    postgresql-contrib

# get the gpg public key
RUN curl -fsSLo /usr/share/keyrings/docker-archive-keyring.asc \
    https://download.docker.com/linux/debian/gpg

RUN echo "deb [arch=$(dpkg --print-architecture) \
    signed-by=/usr/share/keyrings/docker-archive-keyring.asc] \
    https://download.docker.com/linux/debian \
    $(lsb_release -cs) stable" > /etc/apt/sources.list.d/docker.list

RUN apt-get update \
    && apt-get install -y \
    docker-ce-cli