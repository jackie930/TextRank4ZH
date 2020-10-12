import sys
import os
import argparse
import logging
import warnings
import io
import json

import warnings
import numpy as np

warnings.filterwarnings("ignore",category=FutureWarning)

sys.path.append('/opt/program/textrank4zh')

import sys
try:
    reload(sys)
    sys.setdefaultencoding('utf-8')
except:
    pass

import codecs
from textrank4zh import TextRank4Keyword, TextRank4Sentence


with warnings.catch_warnings():
    warnings.filterwarnings("ignore",category=DeprecationWarning)
    # from autogluon import ImageClassification as task

import flask

# The flask app for serving predictions
app = flask.Flask(__name__)

@app.route('/ping', methods=['GET'])
def ping():
    """Determine if the container is working and healthy. In this sample container, we declare
    it healthy if we can load the model successfully."""
    # health = ScoringService.get_model() is not None  # You can insert a health check here
    health = 1

    status = 200 if health else 404
    print("===================== PING ===================")
    return flask.Response(response="{'status': 'Healthy'}\n", status=status, mimetype='application/json')

@app.route('/invocations', methods=['POST'])
def invocations():
    """Do an inference on a single batch of data. In this sample server, we take data as CSV, convert
    it to a pandas data frame for internal use and then convert the predictions back to CSV (which really
    just means one prediction per line, since there's a single column.
    """
    data = None
    print("================ INVOCATIONS =================")
    data = flask.request.data.decode('utf-8')
    print ("<<<<<input data: ", data)
    print ("<<<<<input content type: ", flask.request.content_type)

    # Convert from CSV to pandas
    #if flask.request.content_type == 'application/json':
    data = flask.request.data.decode('utf-8')
    print ("<<<<<input data: ", data)
    data = json.loads(data)
    data_input = data['data']

    print('Invoked with {} records'.format(data.keys()))

    # Do the prediction
    #result = "摘要，关键词"
    tr4w = TextRank4Keyword()
    tr4w.analyze(text=data_input, lower=True, window=2)
    keyword_ls = []
    keyword_weight = []
    for item in tr4w.get_keywords(20, word_min_len=1):
        keyword_ls.append(item.word)
        keyword_weight.append(item.weight)

    tr4s = TextRank4Sentence()
    tr4s.analyze(text=data_input, lower=True, source = 'all_filters')
    summarysentence_ls = []
    summarysentence_location = []
    summarysentence_weight = []
    for item in tr4s.get_key_sentences(num=3):
        summarysentence_ls.append(item.sentence)
        summarysentence_location.append(item.index)
        summarysentence_weight.append(item.weight)

    result = {"关键词列表":keyword_ls,
              "关键词权重":keyword_weight,
              "摘要列表":summarysentence_ls,
              "摘要位置index":summarysentence_location,
              "摘要权重":summarysentence_weight}
    print ("<<<result: ", result)

    x={"res":result}
    response=json.dumps(x,ensure_ascii=False)

    return flask.Response(response=response, status=200, mimetype='application/json')