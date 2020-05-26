FROM ubuntu:18.04

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt && \
	pip3 install ansible[azure]

RUN ln -s /usr/bin/python3 /usr/bin/python

COPY src /ansible
WORKDIR /ansible

COPY docker-entrypoint.sh /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]