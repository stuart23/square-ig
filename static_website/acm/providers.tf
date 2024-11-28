terraform {
  required_version = "~> 1.10.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    porkbun = {
      source  = "cullenmcdermott/porkbun"
      version = "~> 0.2.5"
    }
    time = {
      source  = "hashicorp/time"
      version = "0.12.1"
    }
  }
}

# Configure the AWS Provider
provider "aws" {
  region = "us-east-1"
}

provider "porkbun" {
  api_key    = var.porkbun_api_key
  secret_key = var.porkbun_secret_key
}