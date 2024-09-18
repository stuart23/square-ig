terraform {
  required_version = "~> 1.9.5"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  backend "s3" {
    bucket         = "square-ig-tfstate"
    key            = "state/terraform.tfstate"
    encrypt        = true
    dynamodb_table = "square-ig-tfstate"
  }
}

# Configure the AWS Provider
provider "aws" {
}

# Get authorization credentials to push to ECR
data "aws_ecr_authorization_token" "token" {}

# KMS for ECR
resource "aws_kms_key" "ecr_kms_key" {
  description             = "KMS Key for ECR"
  enable_key_rotation     = true
  deletion_window_in_days = 20
}

# ECR for Lambda Image
resource "aws_ecr_repository" "lambda_ecr" {
  name                 = "lambdaimage"
  image_tag_mutability = "MUTABLE"
  encryption_configuration {
    encryption_type = "KMS"
    kms_key         = aws_kms_key.ecr_kms_key.arn
  }
}

output "ecr_repo_url" {
  value = aws_ecr_repository.lambda_ecr.repository_url
}