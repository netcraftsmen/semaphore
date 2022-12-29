#
#     Copyright (c) 2022 Joel W. King
#     All rights reserved.
#
#     author: @joelwking
#     written:  28 December 2022
#     references:
#       activate virtualenv: https://pythonspeed.com/articles/activate-virtualenv-dockerfile/
#
FROM python:3.8.10-slim-buster
ENV VIRTUAL_ENV=/opt/semaphore
LABEL maintainer="Joel W. King" email="ccie1846@gmail.com"
RUN apt update && \
    apt -y install git && \
    apt -y install python3-venv && \
    pip3 install --upgrade pip 
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
#
#
RUN mkdir /src
COPY requirements.txt /src
WORKDIR /src
RUN pip install -r requirements.txt
#
