# -*- encoding:utf-8 -*-

import pandas as pd
from boto3.session import Session
import json
import glob
import numpy as np
from pyrouge import Rouge155
from pprint import pprint
import collections


def invoke_endpoint(data):
    data = {
        "data": data}
    session = Session()

    runtime = session.client("runtime.sagemaker")
    response = runtime.invoke_endpoint(
        EndpointName='textrank',
        ContentType="application/json",
        Body=json.dumps(data),
    )

    result = json.loads(response["Body"].read())
    # print ("<<<< result: ",''.join(result['res']['摘要列表']))
    return ''.join(result['res']['摘要列表'])


def load_data(txt_folder, i):
    text_name = glob.glob(txt_folder + '/*.txt')[i]
    with open(text_name, "r", encoding="utf-8") as f:
        text = f.read()
    text = text.split('SPLIT')
    if len(text) > 1:
        title = text[0]
        content = text[1]
    pred_title = invoke_endpoint(content)
    return title, pred_title, content


def load_vocab(vocab_file):
    """Loads a vocabulary file into a dictionary."""
    vocab = collections.OrderedDict()
    index = 0
    with open(vocab_file, "r", encoding="utf-8") as reader:
        while True:
            token = reader.readline()
            if not token:
                break
            token = token.strip()
            vocab[token] = index
            index += 1
    return vocab


def convert_cn(input, a):
    output = ""
    for x in input:
        try:
            output = output + ' ' + str(a[x])
        except:
            continue
    return output


def calculate_rouge(ref_texts, summary_text):
    vocab_ls = load_vocab('./bert-base-chinese-vocab.txt')
    # need to install pip install git+https://github.com/tagucci/pythonrouge.gi
    ref_texts = {"A": convert_cn(ref_texts, vocab_ls)}
    summary_text = convert_cn(summary_text, vocab_ls)

    rouge = Rouge155()
    score = rouge.score_summary(summary_text, ref_texts)
    return score


def process_single_file(txt_folder, i):
    title, pred_title, content = load_data(txt_folder, i)
    # print ("title:", title)
    # print ("<<<<<")
    # print ("pred title:", pred_title)
    score = calculate_rouge(title, pred_title)
    # print ("rouge score: ", score)
    return title, pred_title, score['rouge_1_f_score'], score['rouge_2_f_score'], content


def main(txt_folder):
    names = glob.glob(txt_folder + '/*.txt')
    title_ls = []
    pred_title_ls = []
    rouge_1_f_score_ls = []
    rouge_2_f_score_ls = []
    content_ls = []
    for i in range(len(names)):
        print ("process number ", i)
        title, pred_title, rouge_1_f_score, rouge_2_f_score, content = process_single_file(txt_folder, i)
        content_ls.append(content)
        title_ls.append(title)
        pred_title_ls.append(pred_title)
        rouge_1_f_score_ls.append(rouge_1_f_score)
        rouge_2_f_score_ls.append(rouge_2_f_score)

    res = pd.DataFrame({"content": content_ls, \
                        "title": title_ls, \
                        "pred_title": pred_title_ls, \
                        "rouge_1_f_score": rouge_1_f_score_ls, \
                        "rouge_2_f_score": rouge_2_f_score_ls})
    print (res.head())
    res.to_csv('result.csv', index=False, encoding='utf-8')
    print ("finish process!")
    print ("avg rougef1", np.mean(rouge_1_f_score_ls))


if __name__ == '__main__':
    txt_folder = '/home/ec2-user/SageMaker/pyrouge/convert_data'
    main(txt_folder)

