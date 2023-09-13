# Dockerfile for Development Environment with GPU Support

# Get Ubuntu server image with GPU support - just in case we need it later
# CUDA version needs to be lower than the local CUDA version
FROM nvidia/cuda:12.2.0-devel-ubuntu22.04

# Set time zone parameters for tzdata
ARG DEBIAN_FRONTEND="noninteractive"
ENV TZ="Europe/London"

# Three lines below can be used to install Python 3.11 but this seems incompatible with tprchvision
# RUN apt-get update
# RUN apt-get install software-properties-common -y
# RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update
RUN apt-get install --yes --no-install-recommends \
    openssh-client \
    git \
    wget \
    curl \
    ca-certificates \
    python3.10 \
    python3.10-dev \
    python3.10-distutils \
    python3.10-venv \
    build-essential \
    libpq-dev
RUN apt-get clean

# Create virtual environment so we use the right pip etc
RUN python3.10 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip3 --version

# Install pip and python tools
RUN pip3 install -U pip setuptools wheel

# Copy over requirements and install first to cache if we only have code change
COPY requirements_slow.txt talking_text/requirements_slow.txt
COPY requirements_quick.txt talking_text/requirements_quick.txt

# Install pip dependencies for slow stuff
RUN cd talking_text && pip3 install --no-cache-dir -r requirements_slow.txt

# Install pip dependencies for quick stuff
RUN cd talking_text && pip3 install --no-cache-dir -r requirements_quick.txt

# Install other files
COPY . talking_text

# Rename the .env_docker file to .env if it exists - || true is to ignore error if file doesn't exist
# RUN mv -f talking_text/.env_docker talking_text/.env || true

# Environment variables are set in the docker-compose file
# Set working directory (this should really be /usr/src/app but hey ho)
# We should also put this up the top but I can't be arsed to rebuild the container
WORKDIR /talking_text
