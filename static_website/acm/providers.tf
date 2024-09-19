# Configure the AWS Provider
provider "aws" {
  region = "us-east-1"
}

provider "porkbun" {
  api_key = var.porkbun_api_key
  secret_key = var.porkbun_secret_key
}
