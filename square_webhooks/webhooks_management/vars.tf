variable "lambda_image" {
  type        = string
  description = "The image that will be deployed to the lambda function. e.g. 015140017687.dkr.ecr.us-east-1.amazonaws.com/lambdaimage:latest@sha256:7cfe0003e1ceaf054f36d316a2c207bad5455fb372916275eadfbd158f2f06db"
}


variable "alerts_sns_topic_arn" {
  description = "ARN of SNS Topic to send alerts to"
  type        = string
}


variable "env_prefix" {
  description = "Prefix for all the resources, e.g. dev, stage, prod"
  type        = string
}


variable "catalog_update_endpoint" {
  description = "URL of the catalog update endpoint"
  type        = string
}