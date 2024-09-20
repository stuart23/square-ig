# Static Website

This directory contains the terraform infrastructure to setup the following to serve a static website:

- AWS S3 to store the assets
- Porkbun for DNS records
- AWS ACM to generate and manage the SSL Certificate
- AWS Cloudformation as the CDN and provide TLS termination.

This can be deployed with terraform locally, or with the Github Action in this repository `deploy-static-website`. The AWS account first needs to be bootstrapped with the infrastructure in /bootstrap to provide the role that Github can assume to deploy via Actions, and to setup the Terraform backend.

Once the infrastructure is deployed, you can go ahead and upload the websites static assets to the bucket in AWS with the same name as the domain name given to Terraform.