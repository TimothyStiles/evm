FROM ubuntu:14.04

MAINTAINER Tim Stiles <tim@stiles.io> 
# based on elenaalexandrovna/opencv-python3 base image

RUN apt-get update && \
    apt-get install -y \
    build-essential \
    cmake \
    git \
    wget \
    unzip \
    pkg-config \
    libswscale-dev \
    python3-dev \
    python3-numpy \
    libtbb2 \
    libtbb-dev \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    libjasper-dev \
    libavformat-dev \
    libgtk2.0-dev \
    pkg-config \
    
    && apt-get -y clean all \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /

RUN cv_version='3.2.0' \
    && wget https://github.com/Itseez/opencv/archive/"$cv_version".zip \
    && unzip "$cv_version".zip \
    && mkdir /opencv-"$cv_version"/cmake_binary \
    && cd /opencv-"$cv_version"/cmake_binary \
    && cmake .. \
    && make install \
    && rm /"$cv_version".zip \
    && rm -r /opencv-"$cv_version"

RUN wget https://bootstrap.pypa.io/get-pip.py \
&& python3 get-pip.py \
&& rm get-pip.py

COPY requirements.txt /tmp/
RUN pip3 install --requirement /tmp/requirements.txt
COPY . /tmp/

COPY . /evm
WORKDIR /evm

CMD ["bash"]
