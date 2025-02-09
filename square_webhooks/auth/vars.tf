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


variable "alerts_sns_topic_arn" {
  description = "ARN of SNS Topic to send alerts to"
  type        = string
}


variable "env_prefix" {
  description = "Prefix for all the resources, e.g. dev, stage, prod"
  type        = string
}


variable "tenants_table" {
  description = "Name of the tenants table"
  type        = string
}


variable "tenants_access_policy_arn" {
  description = "Arn of the policy for accessing the tenants table."
  type        = string
}


variable "write_metrics_policy_arn" {
  description = "Arn of the policy for writing metrics to cloudwatch."
  type        = string
}


variable "lambda_assume_role_policy" {
  description = "Assume role policy to allow lambda function to call role."
  type        = string
}