FROM elenaalexandrovna/opencv-python3

MAINTAINER Tim Stiles <tim@stiles.io>

RUN wget https://bootstrap.pypa.io/get-pip.py \
&& python3 get-pip.py \
&& rm get-pip.py

COPY requirements.txt /tmp/
RUN pip3 install --requirement /tmp/requirements.txt
COPY . /tmp/

COPY . /evm
WORKDIR /evm

CMD ["python3"]
