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
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ flask gevent gunicorn

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

# Copy pretrained model
#COPY resnet50_cars-0000.params /opt/program/
#COPY resnet50_cars-symbol.json /opt/program/
#COPY classes.txt /opt/program/

WORKDIR /opt/program

ENTRYPOINT ["python", "serve.py"]

