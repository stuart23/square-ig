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


variable "tenants_read_only_policy_arn" {
  type        = string
  description = "The arn of the iam role used to read the tenants table"
}


variable "catalog_read_write_policy_arn" {
  type        = string
  description = "The arn of the iam role used to read and write to the catalog table"
}


variable "tenants_table_name" {
  type        = string
  description = "The name of the tenants table"
}


variable "catalog_table_name" {
  type        = string
  description = "The name of the catalog table"
}


# variable "square_authorizer_id" {
#   type        = string
#   description = "ID of the authorizer to only allow square IP addresses"
# }


variable "generate_label_sns_topic_arn" {
  type        = string
  description = "ARN of the SNS topic to publish events to."
}


variable "generate_label_sns_publish_policy_arn" {
  type        = string
  description = "ARN of the policy that allows publishing to the sns topic."
}


variable "alerts_sns_topic_arn" {
  description = "ARN of SNS Topic to send alerts to"
  type        = string
}


variable "env_prefix" {
  description = "Prefix for all the resources, e.g. dev, stage, prod"
  type        = string
}


variable "lambda_assume_role_policy" {
  description = "Assume role policy to allow lambda function to call role."
  type        = string
}