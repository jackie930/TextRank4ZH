ARG REGISTRY_URI
FROM ${REGISTRY_URI}/mxnet-inference:1.6.0-cpu-py3

RUN mkdir -p /opt/ml/model

# COPY package/ /opt/ml/code/package/

# COPY serve.py /opt/ml/model/code/

ENV PYTHONUNBUFFERED=TRUE
ENV PYTHONDONTWRITEBYTECODE=TRUE
ENV PATH="/opt/program:${PATH}"

##########################################################################################
# SageMaker requirements
##########################################################################################
## install flask
RUN pip install networkx==2.3 flask gevent gunicorn jieba==0.42.1 -i https://opentuna.cn/pypi/web/simple

### Install nginx notebook
RUN apt-get -y update && apt-get install -y --no-install-recommends \
         wget \
         nginx \
         ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# forward request and error logs to docker log collector
RUN ln -sf /dev/stdout /var/log/nginx/access.log
RUN ln -sf /dev/stderr /var/log/nginx/error.log

# Set up the program in the image
COPY serve.py /opt/program/
COPY predictor.py /opt/program/
COPY wsgi.py /opt/program/
COPY nginx.conf /opt/program/
COPY textrank4zh/* /opt/program/textrank4zh/

WORKDIR /opt/program

ENTRYPOINT ["python", "serve.py"]

