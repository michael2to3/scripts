FROM ubuntu:latest

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    gnupg2 \
    software-properties-common \
    apt-transport-https \
    ca-certificates \
    neovim \
    openssh-client \
    && rm -rf /var/lib/apt/lists/*

RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" \
    && unzip awscliv2.zip \
    && ./aws/install \
    && rm -rf awscliv2.zip aws

RUN curl -sSL https://storage.yandexcloud.net/yandexcloud-yc/install.sh | bash \
    && echo 'export PATH="$HOME/yandex-cloud/bin:$PATH"' >> ~/.bashrc

ENV PATH="/root/yandex-cloud/bin:${PATH}"

RUN curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" \
    && install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl \
    && rm -f kubectl

RUN curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

CMD ["/bin/bash"]
