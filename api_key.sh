#!/bin/bash

aws secretsmanager create-secret \
    --name my-api-key \
    --description "API key for accessing the Sport Highlights API" \
    --secret-string '{"api_key":"2111b15adcmsh11ffa193ecdd7b8p10ece2jsn0b1449c39037"}' \
    --region us-east-1


    