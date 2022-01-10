FROM python:3.9-slim

RUN apt-get update && apt-get install -y apt-transport-https \
    ca-certificates \
    build-essential \
    libpq-dev \
    python3-dev \
    curl \
    postgresql \
    postgresql-contrib

RUN curl -fsSLo /usr/share/keyrings/kubernetes-archive-keyring.gpg https://packages.cloud.google.com/apt/doc/apt-key.gpg

RUN echo "deb [signed-by=/usr/share/keyrings/kubernetes-archive-keyring.gpg] https://apt.kubernetes.io/ kubernetes-xenial main" | tee /etc/apt/sources.list.d/kubernetes.list

RUN apt-get update && \
    apt-get install -y kubectl

RUN pip install awscli