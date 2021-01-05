# TAG dnastack/plink:1.9
FROM ubuntu:bionic

MAINTAINER Heather Ward <heather@dnastack.com>

RUN apt-get -qq update && \
	apt-get -qq install \
	wget \
	unzip \
	gawk \
	python3-dev \
	python3-pip

# PLINK v1.9
RUN mkdir /opt/plink
RUN wget http://s3.amazonaws.com/plink1-assets/dev/plink_linux_x86_64.zip && \
        unzip -d /opt/plink plink_linux_x86_64.zip && \
        rm plink_linux_x86_64.zip

RUN ln -s /opt/plink/plink /usr/local/bin/

COPY ./requirements.txt /opt/requirements.txt

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -r /opt/requirements.txt

COPY ./scripts/* /usr/local/bin/
