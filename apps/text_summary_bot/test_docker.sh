set -x
user_id=$1
ak=$2
sk=$3


 docker run --rm \
    -e region_name='us-east-1' \
    -e endpoint_name='bert_sentiment' \
    -e output_s3_bucket='spot.bot.asset' \
    -e aws_access_key_id="${ak}" \
    -e aws_secret_access_key="${sk}" \
    -e batch_id='2' \
    -e job_id='f0a96351-9b01-402d-9ee2-51b91a86ac5f' \
    -e es_protocol='http' \
    -e es_index='spot_bot' \
    -e es_host='3.234.47.83' \
    -e es_port='80' \
    "${user_id}".dkr.ecr.us-east-1.amazonaws.com/sentiment_analysis_bot
