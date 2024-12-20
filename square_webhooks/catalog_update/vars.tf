variable "lambda_image" {
  type        = string
  description = "The image that will be deployed to the lambda function. e.g. 015140017687.dkr.ecr.us-east-1.amazonaws.com/lambdaimage:latest@sha256:7cfe0003e1ceaf054f36d316a2c207bad5455fb372916275eadfbd158f2f06db"
}


variable "square_gateway_id" {
  type        = string
  description = "The id of the square_gateway aws_apigatewayv2_api resource"
}


variable "square_gateway_execution_arn" {
  type        = string
  description = "The execution arn of the square_gateway aws_apigatewayv2_api resource"
}


variable "lambda_role_arn" {
  type        = string
  description = "The arn of the iam role used to execute the lambda function"
}


variable "square_authorizer_id" {
  type        = string
  description = "ID of the authorizer to only allow square IP addresses"
}


variable "generate_label_sns_topic_arn" {
  type        = string
  description = "ARN of the SNS topic to publish events to."
}


variable "square_token_arn" {
  type        = string
  description = "ARN of the secret containing the square token."
}


variable "alerts_sns_topic_arn" {
  description = "ARN of SNS Topic to send alerts to"
  type        = string
}


variable "instructions_git_repo" {
  description = "Github repo for instructions"
  type        = string
}


variable "gh_key_arn" {
  description = "KMS ARN for the git ssh private key"
  type        = string
}