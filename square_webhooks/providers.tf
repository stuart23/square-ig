terraform {
  required_version = "~> 1.10.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  backend "s3" {
    bucket         = "square-qr-tfstate"
    encrypt        = true
    dynamodb_table = "square-qr-tfstate"
  }
}

# Configure the AWS Provider
provider "aws" {
  region = var.aws_region
}