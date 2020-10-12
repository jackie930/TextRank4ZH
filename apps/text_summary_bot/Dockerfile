ARG REGISTRY_URI
FROM ${REGISTRY_URI}/mxnet-inference:1.6.0-cpu-py3

ENV PYTHONUNBUFFERED=TRUE
ENV PYTHONDONTWRITEBYTECODE=TRUE

ENV LANG=en_US.utf8
COPY . /tmp
WORKDIR /tmp
RUN pip install boto3 -i https://opentuna.cn/pypi/web/simple
RUN pip install elasticsearch==7.8.0 -i https://opentuna.cn/pypi/web/simple
RUN pip install requests -i https://opentuna.cn/pypi/web/simple
#CMD ["python","-u","/tmp/task.py"]
ENTRYPOINT ["python", "/tmp/task.py"]