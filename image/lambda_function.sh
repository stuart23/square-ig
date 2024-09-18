#!/bin/bash

# # In a lambda function, all directories except /tmp are read-only, so we need to write in there.
# mkdir -p /tmp/dags
# mkdir -p /tmp/home
# export HOME=/tmp/home

cd /tmp/astro

# Create 
astro dev init
# Sync the Astro deployment from S3 to the local directory
aws s3 sync s3://dagsdeploy /tmp/astro/dags --delete

# Get the API token from AWS Secrets Manager. The name of the secret,
# `astro_api_token_secret_name`, comes from the Lambda function execution environment
export ASTRO_API_TOKEN=$(aws secretsmanager get-secret-value --secret-id $astro_api_token_secret_name --query SecretString --output text)

# We enable dag-deployments, which is redundant except for the first run.
astro deployment update --dag-deploy enable

# Finally deploy the dags.
astro deploy --dags