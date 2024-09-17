terraform {
  required_version = "~> 1.9.5"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Configure the AWS Provider
provider "aws" {
  region = "us-west-1"
}

# KMS for ECR
resource "aws_kms_key" "kms_key" {
  description             = "KMS Key"
  enable_key_rotation     = true
  deletion_window_in_days = 20
}