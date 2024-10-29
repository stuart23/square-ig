terraform {
  required_version = "~> 1.9.5"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    porkbun = {
      source  = "cullenmcdermott/porkbun"
      version = "~> 0.2.5"
    }
  }
  backend "s3" {
    bucket         = "square-ig-tfstate"
    key            = "static_website/terraform.tfstate"
    encrypt        = true
    dynamodb_table = "square-ig-tfstate"
  }
}

# Configure the AWS Provider
provider "aws" {
  region = var.aws_region
}

provider "porkbun" {
  api_key    = var.porkbun_api_key
  secret_key = var.porkbun_secret_key
}