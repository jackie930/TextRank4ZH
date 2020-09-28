#!/bin/bash
# set -x
# This script shows how to build the Docker image and push it to ECR to be ready for use
# by SageMaker.

# The argument to this script is the image name. This will be used as the image on the local
# machine and combined with the account and region to form the repository name for ECR.
image=$1
profile=$2

if [ "$image" == "" ]
then
    echo "Use image name text-summary-bot"
    image="text-summary--bot"
fi

if [ "$profile" == "" ]
then
    echo "Use profile=default"
    profile="default"
fi

# Get the account number associated with the current IAM credentials
account=$(aws --profile ${profile} sts get-caller-identity --query Account --output text)

if [ $? -ne 0 ]
then
    exit 255
fi

# Get the region defined in the current configuration
# region=$(aws --profile ${profile} configure get region)
regions=$(aws ec2 describe-regions --all-regions --query "Regions[].{Name:RegionName}" --output text)
#regions="eu-north-1 ap-south-1 eu-west-3 eu-west-2 eu-west-1 ap-northeast-3 ap-northeast-2 me-south-1 ap-northeast-1 sa-east-1 ca-central-1 ap-east-1 ap-southeast-1 ap-southeast-2 eu-central-1 us-east-1 us-east-2 us-west-1 us-west-2"

for region in $regions; do

if [[ $region =~ ^cn.* ]]
then
    fullname="${account}.dkr.ecr.${region}.amazonaws.com.cn/${image}:latest"
else
    fullname="${account}.dkr.ecr.${region}.amazonaws.com/${image}:latest"
fi

echo ${fullname}

# If the repository doesn't exist in ECR, create it.
aws --profile ${profile} ecr describe-repositories --repository-names "${image}" --region ${region}

if [ $? -ne 0 ]
then
    aws --profile ${profile} ecr create-repository --repository-name "${image}" --region ${region} > /dev/null
fi

#set cross account pull policy
aws --profile ${profile} ecr set-repository-policy \
    --repository-name "${image}" \
    --policy-text "file://../ecr-policy.json"

# Get the login command from ECR and execute it directly
$(aws --profile ${profile} ecr get-login --registry-ids ${account} --region ${region} --no-include-email)

# Build the docker image, tag with full name and then push it to ECR
docker build -t ${image} -f Dockerfile .
docker tag ${image} ${fullname}
docker push ${fullname}

done


