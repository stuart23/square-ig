variable "lambda_image" {
  type        = string
  description = "The image that will be deployed to the lambda function. e.g. 015140017687.dkr.ecr.us-east-1.amazonaws.com/lambdaimage:latest@sha256:7cfe0003e1ceaf054f36d316a2c207bad5455fb372916275eadfbd158f2f06db"
}

variable "aws_region" {
  type        = string
  description = "The region to deploy into"
}

variable "square_token" {
  description = "Token for accessing Square"
  type        = string
  sensitive   = true
}

variable "instagram_username" {
  description = "Instagram Username"
  type        = string
  sensitive   = true
}

variable "instagram_password" {
  description = "Instagram Password"
  type        = string
  sensitive   = true
}