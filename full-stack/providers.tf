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
    key            = "square_ig/terraform.tfstate"
    encrypt        = true
    dynamodb_table = "square-ig-tfstate"
  }
}

# Configure the AWS Provider
provider "aws" {
  region = "us-west-1"
}