# day5-MediaConverter-

## Introduction

This is an application that download a video from the API. It then stores the video in S3. The Video is then taken by media converter and converted to a different format. The converted video is then stored in S3. The application then sends a notification to the user that the video has been converted.

## System Design

![System Design](image/media_converter.png)

## Installation

##### set up Python with uv:

```bash
uv venv <env-name> --python 3.11
source <env-name>/bin/activate
uv pip install -r requirements.txt
```

##### Deploy the CloudFormation Stack

```bash
aws cloudformation create-stack --stack-name jsonb5 --template-body file://json_bucket.yaml --capabilities CAPABILITY_NAMED_IAM
```

##### Attach the iam policy

```bash
aws iam create-policy \
 --policy-name MyUpdatedMediaConvertPolicy \
 --policy-document file://managed-policy.json \
 --profile your-profile

aws iam attach-user-policy \\n  --user-name <user-name> \\n  --policy-arn arn:aws:iam::<account number></account>:policy/MyUpdatedMediaConvertPolicy
```

##### Create the ecr repository

```bash
 aws ecr create-repository --repository-name highlight-pipeline
```

##### log into the ecr repository

```bash
aws ecr get-login-password --region <REGION> | docker login --username AWS --password-stdin <AWS_ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com
```

##### Build the docker image

```bash
docker build -t highlight-pipeline:latest .
docker tag highlight-pipeline:latest <AWS_ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com/highlight-pipeline:latest
```

##### Push the docker image

```bash
docker push <AWS_ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com/highlight-pipeline:latest
```

##### Destroy the ECR container

```bash
aws ecr delete-repository --repository-name highlight-pipeline --force
```

##### Destroy the Terraform infrastructure

```bash

terraform destroy -auto-approve
```
