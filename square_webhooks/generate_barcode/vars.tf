variable "lambda_image" {
  type        = string
  description = "The image that will be deployed to the lambda function. e.g. 015140017687.dkr.ecr.us-east-1.amazonaws.com/lambdaimage:latest@sha256:7cfe0003e1ceaf054f36d316a2c207bad5455fb372916275eadfbd158f2f06db"
}


variable "lambda_role_arn" {
  type        = string
  description = "The arn of the iam role used to execute the lambda function"
}


variable "square_token_arn" {
  type        = string
  description = "ARN of the secret containing the square token."
}


variable "alerts_sns_topic_arn" {
  description = "ARN of SNS Topic to send alerts to"
  type        = string
}