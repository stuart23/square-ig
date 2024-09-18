terraform {
  required_version = "~> 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Configure the AWS Provider
provider "aws" {
  region = "us-east-1"
}

variable "github_org_name" {
  type        = string
  default     = "stuart23"
  description = "The GitHub user or organization that contains the repo that will run actions as this role."
}

variable "github_repo_name" {
  type        = string
  default     = "square-ig"
  description = "The GitHub repo that will run actions as this role."
}

module "iam_github_oidc_role" {
  name        = "GithubCICDRole"
  description = "Github Actions role for repo ${var.github_org_name}/${var.github_repo_name}"
  source      = "terraform-aws-modules/iam/aws//modules/iam-github-oidc-role"
  subjects    = ["${var.github_org_name}/${var.github_repo_name}:*"]
  policies = {
    Admin = "arn:aws:iam::aws:policy/AdministratorAccess"
  }
}

# resource "aws_iam_openid_connect_provider" "github" {
#   url = "https://token.actions.githubusercontent.com"
#   client_id_list = [
#     "sts.amazonaws.com",
#   ]
#   thumbprint_list = [
#     "6938fd4d98bab03faadb97b34396831e3780aea1",
#     "1c58a3a8518e8759bf075b76b750d4f2df264fcd"
#   ]
# }

# # IAM policy for retrieving Secrets from SecretsManager
# resource "aws_iam_policy" "read_secret" {
#   name        = "read_secret"
#   description = "Read secrets used in lambda function"
#   policy = jsonencode({
#     Version = "2012-10-17"
#     Statement = [
#       {
#         Action = [
#           "secretsmanager:GetRandomPassword",
#           "secretsmanager:GetResourcePolicy",
#           "secretsmanager:GetSecretValue",
#           "secretsmanager:DescribeSecret",
#           "secretsmanager:ListSecretVersionIds",
#           "secretsmanager:ListSecrets",
#           "secretsmanager:BatchGetSecretValue",
#         ]
#         Effect   = "Allow"
#         Resource = "*"
#       },
#     ]
#   })
# }

# resource "aws_iam_role" "cicd_role" {
#   name = "cicd_role"
#   assume_role_policy = jsonencode({
#     Version = "2012-10-17"
#     Statement = [
#       {
#         Action = "sts:AssumeRoleWithWebIdentity"
#         Effect = "Allow"
#         Principal = {
#           Federated = [ aws_iam_openid_connect_provider.github.arn]
#         }
#         Condition = {
#           StringLike = {

#           }
#         }
#       },
#     ]
#   })
# }

# resource "aws_iam_role_policy_attachment" "admin_policy_attachment" {
#   role       = aws_iam_role.cicd_role.name
#   policy_arn = "arn:aws:iam::aws:policy/AdministratorAccess"
# }

output "role_arn" {
  value = "${var.github_org_name}/${var.github_repo_name}:*"
  # value = module.iam_github_oidc_role.arn
}