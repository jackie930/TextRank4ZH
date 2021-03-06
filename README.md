# TextRank4ZH

TextRank算法可以用来从文本中提取关键词和摘要（重要的句子）。TextRank4ZH是针对中文文本的TextRank算法的python算法实现。

## 安装

方式1：
```
$ python setup.py install --user
```

方式2：
```
$ sudo python setup.py install
```

方式3：
```
$ pip install textrank4zh --user
```

方式4：
```
$ sudo pip install textrank4zh
```

Python 3下需要将上面的python改成python3，pip改成pip3。


## 卸载
```plain
$ pip uninstall textrank4zh
```

## 依赖
jieba >= 0.35  
numpy >= 1.7.1  
networkx >= 1.9.1  

## 兼容性
在Python 2.7.9和Python 3.4.3中测试通过。


## 原理

TextRank的详细原理请参考：

> Mihalcea R, Tarau P. TextRank: Bringing order into texts[C]. Association for Computational Linguistics, 2004.

关于TextRank4ZH的原理和使用介绍：[使用TextRank算法为文本生成关键字和摘要](https://www.letiantian.me/2014-12-01-text-rank/)

### 关键词提取
将原文本拆分为句子，在每个句子中过滤掉停用词（可选），并只保留指定词性的单词（可选）。由此可以得到句子的集合和单词的集合。

每个单词作为pagerank中的一个节点。设定窗口大小为k，假设一个句子依次由下面的单词组成：
```
w1, w2, w3, w4, w5, ..., wn
```
`w1, w2, ..., wk`、`w2, w3, ...,wk+1`、`w3, w4, ...,wk+2`等都是一个窗口。在一个窗口中的任两个单词对应的节点之间存在一个无向无权的边。

基于上面构成图，可以计算出每个单词节点的重要性。最重要的若干单词可以作为关键词。


### 关键短语提取
参照[关键词提取](#关键词提取)提取出若干关键词。若原文本中存在若干个关键词相邻的情况，那么这些关键词可以构成一个关键词组。

例如，在一篇介绍`支持向量机`的文章中，可以找到关键词`支持`、`向量`、`机`，通过关键词组提取，可以得到`支持向量机`。

### 摘要生成
将每个句子看成图中的一个节点，若两个句子之间有相似性，认为对应的两个节点之间有一个无向有权边，权值是相似度。

通过pagerank算法计算得到的重要性最高的若干句子可以当作摘要。


## 示例
见[example](./example)、[test](./test)。

## 使用说明

类TextRank4Keyword、TextRank4Sentence在处理一段文本时会将文本拆分成4种格式：

* sentences：由句子组成的列表。
* words_no_filter：对sentences中每个句子分词而得到的两级列表。
* words_no_stop_words：去掉words_no_filter中的停止词而得到的二维列表。
* words_all_filters：保留words_no_stop_words中指定词性的单词而得到的二维列表。


# 本地部署

server 
```shell script
cd apps/text_summry_endpoint
sh build_and_push.sh
docker run -v -d -p 8080:8080 textrank
```
client

```python
# test 
#curl http://localhost:8080/ping 

# curl
import requests
import json

url='http://localhost:8080/invocations'
data={"data": "《半導體》Q1展望保守，世界垂淚2019/02/11 10:28時報資訊【時報記者沈培華台北報導】世界先進 (5347) 去年營運創歷史新高，每股純益達3.72元。但對今年首季展望保守，預計營收將比上季高點減近一成。世界先進於封關前股價拉高，今早則是開平走低。世界先進於年前台股封關後舉行法說會公布財報。公司去年營運表現亮麗，營收與獲利同創歷史新高紀錄。2018年全年營收289.28億元，年增16.1%，毛利率35.2%，拉升3.2個百分點，稅後淨利61.66億元，年增36.9%，營收與獲利同創歷史新高，每股純益3.72元。董事會通過去年度擬配發現金股利3.2元。展望第一季，受到客戶進入庫存調整，公司預期，本季營收估在67億至71億元，將季減8%至13%，毛利率將約34.5%至36.5%。此外，因應客戶需求，世界先進決定斥資2.36億美元，收購格芯新加坡8吋晶圓廠。世界先進於年前宣布，將購買格芯位於新加坡Tampines的8吋晶圓3E廠房、廠務設施、機器設備及微機電(MEMS)智財權與業務，交易總金額2.36億美元，交割日訂108年12月31日。格芯晶圓3E廠現有月產能3.5萬片8吋晶圓，世界先進每年將可增加超過40萬片8吋晶圓產能，增進公司明年起業績成長動能。TOP關閉"}
data = json.dumps(data)
r = requests.post(url,data=data)

#show result
print (r.text)
```

结果如下
```json
{"res": {"关键词列表": ["公司", "後", "於", "客戶", "世界", "會", "歷史", "展望", "高點", "定斥", "保守", "去年", "年度", "金", "廠務", "智", "時報", "擬配", "發現", "公布"], 
"关键词权重": [0.021830182644348436, 0.021326461850579626, 0.021079603384026722, 0.01895223347929955, 0.01805834763586865, 0.015857085161081398, 0.014919166963726964, 0.01471938511506705, 0.014620888893926702, 0.014620888893926702, 0.014001573075273081, 0.013746893722718052, 0.011987812728358822, 0.011987812728358822, 0.011643071195825557, 0.011643071195825555, 0.011533578138425806, 0.011474480918306437, 0.011474480918306437, 0.011389711378308801], 
"摘要列表": ["《半導體》Q1展望保守，世界垂淚2019/02/11 10:28時報資訊【時報記者沈培華台北報導】世界先進 (5347) 去年營運創歷史新高，每股純益達3.72元", "世界先進於年前宣布，將購買格芯位於新加坡Tampines的8吋晶圓3E廠房、廠務設施、機器設備及微機電(MEMS)智財權與業務，交易總金額2.36億美元，交割日訂108年12月31日", "格芯晶圓3E廠現有月產能3.5萬片8吋晶圓，世界先進每年將可增加超過40萬片8吋晶圓產能，增進公司明年起業績成長動能"], 
"摘要位置index": [0, 9, 10], "摘要权重": [0.1061431564717524, 0.10339832449272994, 0.09211266281495177]}}
```
## 使用rouge指标评估

###安装pyrouge

```shell script
sudo yum -y install perl-CPAN
sudo cpan YAML
sudo cpan Module::Metadata
sudo cpan Module::Build
sudo cpan IO::Socket
sudo cpan IO::Socket::IP
sudo cpan HTTP::Daemon
sudo cpan LWP::UserAgent
sudo cpan DB_File

cd pyrouge

cd tools/ROUGE-1.5.5/data/
rm WordNet-2.0.exc.db
./WordNet-2.0-Exceptions/buildExeptionDB.pl ./WordNet-2.0-Exceptions ./smart_common_words.txt ./WordNet-2.0.exc.db

pyrouge_set_rouge_path /home/ec2-user/SageMaker/pyrouge/tools/ROUGE-1.5.5

cd ../../../
pyrouge_set_rouge_path /home/ec2-user/SageMaker/pyrouge/tools/ROUGE-1.5.5
python setup.py install
```

### 测试评估

```shell script
python test_rouge.py
```

结果产生为如下格式的结果表

| 原文 | 标注摘要 | 生成摘要 |评估指标rouge1 |评估指标rouge2 |
| ------ | ------ | ------ |------ |------|
| text | text | text |number |number|



## Deploy endpoint on SageMaker 
```shell script
endpoint_ecr_image="251885400447.dkr.ecr.cn-northwest-1.amazonaws.com.cn/textrank"
python create_endpoint.py \
--endpoint_ecr_image_path ${endpoint_ecr_image} \
--endpoint_name 'textrank' \
--instance_type "ml.t2.medium"
```

在部署结束后，看到SageMaker控制台生成了对应的endpoint,可以使用如下客户端代码测试调用
```python
from boto3.session import Session
import json
data={"data": "《半導體》Q1展望保守，世界垂淚2019/02/11 10:28時報資訊【時報記者沈培華台北報導】世界先進 (5347) 去年營運創歷史新高，每股純益達3.72元。但對今年首季展望保守，預計營收將比上季高點減近一成。世界先進於封關前股價拉高，今早則是開平走低。世界先進於年前台股封關後舉行法說會公布財報。公司去年營運表現亮麗，營收與獲利同創歷史新高紀錄。2018年全年營收289.28億元，年增16.1%，毛利率35.2%，拉升3.2個百分點，稅後淨利61.66億元，年增36.9%，營收與獲利同創歷史新高，每股純益3.72元。董事會通過去年度擬配發現金股利3.2元。展望第一季，受到客戶進入庫存調整，公司預期，本季營收估在67億至71億元，將季減8%至13%，毛利率將約34.5%至36.5%。此外，因應客戶需求，世界先進決定斥資2.36億美元，收購格芯新加坡8吋晶圓廠。世界先進於年前宣布，將購買格芯位於新加坡Tampines的8吋晶圓3E廠房、廠務設施、機器設備及微機電(MEMS)智財權與業務，交易總金額2.36億美元，交割日訂108年12月31日。格芯晶圓3E廠現有月產能3.5萬片8吋晶圓，世界先進每年將可增加超過40萬片8吋晶圓產能，增進公司明年起業績成長動能。TOP關閉"}

session = Session()
    
runtime = session.client("runtime.sagemaker")
response = runtime.invoke_endpoint(
    EndpointName='textrank',
    ContentType="application/json",
    Body=json.dumps(data),
)

result = json.loads(response["Body"].read())
print (result)
```

## Deploy via Spot Tagging Bot
在确保可以部署成功endpint的情况下，我们可以将此功能注册为一个新的机器人。
```shell script
cd apps/text_summry_bot
sh build_and_push.sh
```

在api gateway中启动一个机器人任务范例提交
```shell script
{
"s3_bucket": "spot-bot-asset",
"s3_path": "text_summary_bot/input",
"bot_name": "text_summary_bot",
"number_of_bots": "1",
"bulk_size": "500",
"output_s3_bucket": "spot-bot-asset",
"output_s3_prefix": "text_summary_bot/output"
}
```

## License
[MIT](./LICENSE)









