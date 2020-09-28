FROM tensorflow/tensorflow:1.15.2-gpu-py3

ENV LANG=en_US.utf8
COPY . /tmp
WORKDIR /tmp
RUN pip install boto3 -i https://opentuna.cn/pypi/web/simple
RUN pip install elasticsearch==7.8.0 -i https://opentuna.cn/pypi/web/simple
RUN pip install requests -i https://opentuna.cn/pypi/web/simple
CMD ["python","-u","/tmp/task.py"]