FROM tstiles/opencv-python3-plus

MAINTAINER Tim Stiles <tim@stiles.io> 
# based on elenaalexandrovna/opencv-python3 base image

COPY requirements.txt /tmp/
RUN pip3 install --requirement /tmp/requirements.txt
COPY . /tmp/

COPY . /evm
WORKDIR /evm

CMD ["bash"]
