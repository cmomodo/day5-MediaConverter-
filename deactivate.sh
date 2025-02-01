#!/bin/bash

# Define the stack name
STACK_NAME="<stack_name>"
USER_NAME="<user_name>"
ACCOUNT_NUMBER="<account_number>"

# Delete the CloudFormation stack
aws cloudformation delete-stack --stack-name "$STACK_NAME"

# Wait for the stack to be deleted
echo "Waiting for stack $STACK_NAME to be deleted..."
aws cloudformation wait stack-delete-complete --stack-name "$STACK_NAME"

# Confirm deletion
if [ $? -eq 0 ]; then
    echo "Stack $STACK_NAME has been successfully deleted."
else
    echo "Failed to delete stack $STACK_NAME."
    echo "Investigate the reason for the failure using the AWS Management Console."
fi

