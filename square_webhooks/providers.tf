terraform {
  required_version = "~> 1.9.5"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    google = {
      source  = "hashicorp/google"
      version = "~> 6.9.0"
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
  region = var.aws_region
}

# Configure the GCP Provider
provider "google" {
  project = var.gcp_project
  # region  = var.gcp_region
}