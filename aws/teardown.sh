#!/bin/bash
AWS_ID=$(aws sts get-caller-identity --query Account --output text)

echo "**** Step: Deleting bucket ****"
aws s3 rm s3://pyrise --recursive --output text >> logs/teardown.log
aws s3api delete-bucket --bucket pyrise --output text >> logs/teardown.log

echo "**** Step: Removing Lambda functions & associated artifacts ****"
aws lambda delete-function \
    --function-name pyrise-service \
    --output text > logs/teardown.log

echo "**** Step: Deleting associated IAM role and attached policy ****"
aws iam detach-role-policy \
    --role-name AWSLambdaS3Role \
    --policy-arn arn:aws:iam::$AWS_ID:policy/AWSLambdaS3Policy \
    --output text >> logs/teardown.log

aws iam delete-role \
    --role-name AWSLambdaS3Role \
    --output text >> logs/teardown.log

aws iam delete-policy \
    --policy-arn arn:aws:iam::$AWS_ID:policy/AWSLambdaS3Policy \
    --output text >> logs/teardown.log

echo "**** Step: Removing local configuration / logging files ****"
rm ./logs/setup.log