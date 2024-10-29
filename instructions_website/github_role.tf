variable "github_org_name" {
  type        = string
  default     = "stuart23"
  description = "The GitHub user or organization that will be able to push to the S3 bucket."
}

variable "github_repo_name" {
  type        = string
  default     = "plantsoc.com"
  description = "The GitHub repo that will be able to push to the S3 bucket."
}

resource "aws_iam_openid_connect_provider" "github" {
  url = "https://token.actions.githubusercontent.com"
  client_id_list = [
    "sts.amazonaws.com",
  ]
  thumbprint_list = [
    "6938fd4d98bab03faadb97b34396831e3780aea1",
    "1c58a3a8518e8759bf075b76b750d4f2df264fcd"
  ]
}

resource "aws_iam_role" "s3_upload_role" {
  name = "s3_upload_role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRoleWithWebIdentity"
        Effect = "Allow"
        Principal = {
          Federated = [aws_iam_openid_connect_provider.github.arn]
        }
        Condition = {
          StringLike = {
            "token.actions.githubusercontent.com:sub" = "repo:${var.github_org_name}/${var.github_repo_name}:*"
          }
          StringEquals = {
            "token.actions.githubusercontent.com:aud" = "sts.amazonaws.com"
          }
        }
      },
    ]
  })
}


resource "aws_iam_policy" "s3_write_policy" {
  name        = "s3_write_policy"
  description = "Write to the S3 bucket"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action   = "s3:PutObject"
        Effect   = "Allow"
        Resource = aws_s3_bucket.website_bucket.arn
      },
    ]
  })
}


resource "aws_iam_role_policy_attachment" "s3_upload_role_policy" {
  role       = aws_iam_role.cicd_role.name
  policy_arn = aws_iam_policy.s3_write_policy.arn
}


output "cicd_role_arn" {
  description = "GitHub action role"
  value       = aws_iam_role.cicd_role.arn
}