# SOURCE: https://github.com/hashicorp/terraform-dynamic-credentials-setup-examples/blob/main/aws/aws.tf

# Copyright (c) HashiCorp, Inc.
# SPDX-License-Identifier: MPL-2.0

provider "aws" {
}

# Data source used to grab the TLS certificate for Terraform Cloud.
#
# https://registry.terraform.io/providers/hashicorp/tls/latest/docs/data-sources/certificate
data "tls_certificate" "tfc_certificate" {
  url = "https://${var.tfc_hostname}"
}

# Creates an OIDC provider which is restricted to
#
# https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_openid_connect_provider
resource "aws_iam_openid_connect_provider" "tfc_provider" {
  url             = data.tls_certificate.tfc_certificate.url
  client_id_list  = [var.tfc_aws_audience]
  thumbprint_list = [data.tls_certificate.tfc_certificate.certificates[0].sha1_fingerprint]
}

# Creates a role which can only be used by the specified Terraform
# cloud workspace.
#
# https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role
resource "aws_iam_role" "terraform_cloud_role" {
  name = "terraform_cloud_role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRoleWithWebIdentity"
        Effect = "Allow"
        Principal = {
          Federated = [ aws_iam_openid_connect_provider.tfc_provider.arn ]
        }
        Condition = {
          StringLike = {
            "${var.tfc_hostname}:sub": "organization:${var.tfc_organization_name}:project:${var.tfc_project_name}:workspace:${var.tfc_workspace_name}:run_phase:*"
          },
          StringEquals: {
            "${var.tfc_hostname}:aud": "${one(aws_iam_openid_connect_provider.tfc_provider.client_id_list)}"
          },
        }
      },
    ]
  })
}

# Creates an attachment to associate the above policy with the
# previously created role.
#
# https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role_policy_attachment
resource "aws_iam_role_policy_attachment" "admin_policy_attachment" {
  role       = aws_iam_role.terraform_cloud_role.name
  policy_arn = "arn:aws:iam::aws:policy/AdministratorAccess"
}