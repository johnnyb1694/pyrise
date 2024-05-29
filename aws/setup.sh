#!/bin/bash
trap remove_staging_files EXIT
remove_staging_files() {
    rm -r staging/* > /dev/null 2>&1
}

echo "**** Step: Retrieving AWS credentials (NB: requires prior SSO login) ****"
AWS_ID=$(aws sts get-caller-identity --query Account --output text)
AWS_REGION=$(aws configure get region)

echo "**** Step: Creating S3 bucket with alias 'pyrise' ****"
aws s3api create-bucket \
    --bucket pyrise \
    --create-bucket-configuration LocationConstraint=$AWS_REGION \
    --output text > logs/setup.log

echo "**** Step: Installing pyrise into local virtual environment ****"
pip install -q .

echo "**** Step: Uploading Google API credentials to S3 bucket ****"
aws s3api put-object \
    --bucket pyrise \
    --key credentials.json \
    --body ./auth/credentials.json \
    --output text >> logs/setup.log
aws s3api put-object \
    --bucket pyrise \
    --key token.json \
    --body ./auth/token.json \
    --output text >> logs/setup.log

echo "**** Step: Creating relevant policy (permissions) for AWS Lambda ****"
aws iam create-policy \
    --policy-name AWSLambdaS3Policy \
    --policy-document file://aws/permissions/policy.json \
    --output text >> logs/setup.log

echo "**** Step: Creating relevant role for AWS Lambda ****"
aws iam create-role \
    --role-name AWSLambdaS3Role \
    --assume-role-policy-document file://aws/permissions/trust-policy.json \
    --output text >> logs/setup.log

echo "**** Step: Attaching policy (permissions) to newly created role ****"
aws iam attach-role-policy \
    --role-name AWSLambdaS3Role \
    --policy-arn arn:aws:iam::$AWS_ID:policy/AWSLambdaS3Policy \
    --output text >> logs/setup.log

echo "**** Step: Sleeping 10 seconds to allow policy to attach to role ****"
sleep 10

echo "**** Step: Configuring Lambda layer (for external dependencies) ****"

mkdir ./staging/python
cp -r ./.venv/lib ./staging/python
cd ./staging
zip -rq ./layer.zip ./python
rm -r ./python
cd ..

LAYER_PUBLISH_OUTPUT=$(aws lambda publish-layer-version --layer-name pyrise-service-layer \
    --zip-file fileb://staging/layer.zip \
    --compatible-runtimes python3.10 \
    --compatible-architectures "arm64")
    
LAYER_VERSION=$(echo $LAYER_PUBLISH_OUTPUT | jq -r '.Version')

echo "**** Step: Sleeping 10 seconds to allow layer to instantiate ****"
sleep 20

echo "**** Step: Creating Lambda function (to run the email service) ****"
chmod u=rwx,go=r lambda_function.py
zip -rq ./staging/function.zip templates lambda_function.py
aws lambda create-function --function-name pyrise-service \
    --runtime python3.10 \
    --architectures "arm64" \
    --role arn:aws:iam::${AWS_ID}:role/AWSLambdaS3Role \
    --zip-file fileb://staging/function.zip \
    --handler lambda_function.lambda_handler \
    --timeout 60 \
    --output text >> logs/setup.log

aws lambda update-function-configuration \
    --function-name pyrise-service \
    --environment file://auth/env.json \
    --layers "arn:aws:lambda:${AWS_REGION}:${AWS_ID}:layer:pyrise-service-layer:${LAYER_VERSION}" \
    --handler lambda_function.lambda_handler \
    --output text >> logs/setup.log


