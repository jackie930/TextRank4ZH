# -*- coding: utf-8 -*-
# @Time    : 9/28/20 4:43 PM
# @Author  : Jackie
# @File    : test_task.py
# @Software: PyCharm

#!/usr/bin/env python
# encoding: utf-8
from __future__ import print_function

import argparse
import os

import sys

import sys
try:
    reload(sys)
    sys.setdefaultencoding('utf-8')
except:
    pass

import json
from boto3.session import Session
from datetime import datetime

# Hack to print to stderr so it appears in CloudWatch.
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def text_summary_main(s3_path, endpoint_name, output_s3_bucket, output_s3_prefix, region_name):
    """
    function: save json_files back to s3 (key: file name value: tag label)
    :param input_s3_path_list: 读入s3文件路径list
    :param endpoint_path: 保存名称
    """
    session = Session(
        region_name=region_name
    )
    s3 = session.client("s3")
    eprint("start!")

    result = {}
    bucket = s3_path.split("/")[2]
    key = "/".join(s3_path.split("/")[3:])
    file_name = s3_path.split("/")[-1]
    # try:
    # s3.Bucket(bucket).download_file(key, file_name)
    eprint(file_name, key, bucket)
    s3.download_file(Filename=file_name, Key=key, Bucket=bucket)

    # read txt
    eprint("process", s3_path)
    f = open(file_name, "r", encoding="utf-8")
    text = "".join(f.readlines())
    f.close()

    # infer endpoint
    label = bot_infer(session, endpoint_name, text)
    result[s3_path] = label

    # save json file
    json_file = file_name.replace(".txt", ".json")
    with open(json_file, "w") as fw:  # 建议改为.split('.')
        json.dump(result, fw, ensure_ascii=False)
        eprint("write json file success!")

    # output to s3
    print ("<<<< output_s3_prefix: ",output_s3_prefix)
    print ("<<<< upload_key: ",upload_key)
    upload_key=output_s3_prefix+'/'+json_file
    s3.upload_file(Filename=json_file, Key=upload_key, Bucket=output_s3_bucket)
    print("uploaded to s3://{}/{}".format(output_s3_bucket, upload_key))

    # delete file locally
    delete_file(json_file)
    delete_file(file_name)


def delete_file(file):
    """
    delete file
    :param file:
    :return:
    """
    if os.path.isfile(file):
        try:
            os.remove(file)
        except:
            pass



def bot_infer(session, endpoint_name, text):
    """
 function: use endpoint to infer on one single text
    """
    # first preprocess input text
    eprint(endpoint_name)
    eprint ("<<<<<<<< source: ", text)
    data={"data": text}
    eprint ("<<<<<<<< data: ", data)
    runtime = session.client("runtime.sagemaker")
    response = runtime.invoke_endpoint(
        EndpointName=endpoint_name,
        ContentType="application/json",
        Body=json.dumps(data),
    )

    result = json.loads(response["Body"].read())
    eprint ("<<<<<<<< result: ", result)
    # return result
    return str(result)



if __name__ == "__main__":
    eprint(">>> Start execution.")
    s3_path='s3://spot-bot-asset/text_summary_bot/input/test.txt'
    endpoint_name='textrank'
    output_s3_bucket='spot-bot-asset'
    output_s3_prefix='text_summary_bot/output'
    region_name='cn-northwest-1'
    text_summary_main(s3_path, endpoint_name, output_s3_bucket, output_s3_prefix,
                      region_name)
    eprint("<<< Exit.")