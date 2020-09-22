FROM ubuntu:16.04

LABEL bot_name="text-summary"

# Defining some variables used at build time to install Python3
ARG PYTHON=python3
ARG PYTHON_PIP=python3-pip
ARG PIP=pip3
ARG PYTHON_VERSION=3.6.6

    
ENV MODEL_PATH=/opt/ml/model

# Copies code under /opt/ml/code where sagemaker-containers expects to find the script to run
COPY . /opt/ml/code/
WORKDIR /opt/ml/code/

# install Flask version==0.10.1
RUN pip3 install flask==0.10.1

# Defines train.py as script entry point
#ENV SAGEMAKER_PROGRAM train.py
EXPOSE 8080

ENTRYPOINT [ "python3" ]
CMD [ "app.py" ]
