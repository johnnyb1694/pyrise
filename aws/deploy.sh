#!/bin/bash

trap remove_staging_files EXIT
remove_staging_files() {
    rm -r staging/*.zip > /dev/null 2>&1
}

echo "**** Step 1: Retrieving AWS credentials ****"
AWS_ID=$(aws sts get-caller-identity --query Account --output text)
AWS_REGION=$(aws configure get region)

echo "**** Step 2: Creating S3 bucket with alias 'pyrise' ****"
aws s3api create-bucket \
    --bucket pyrise \
    --create-bucket-configuration LocationConstraint=$AWS_REGION \
    --output text > logs/setup.log

