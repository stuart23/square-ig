# Get authorization credentials to push to ECR
data "aws_ecr_authorization_token" "token" {}

# KMS for ECR
resource "aws_kms_key" "ecr_kms_key" {
  description             = "KMS Key for ECR"
  enable_key_rotation     = true
  deletion_window_in_days = 20
}

# ECR for Lambda Image
resource "aws_ecr_repository" "lambda_ecr" {
  name                 = "lambdaimage"
  image_tag_mutability = "MUTABLE"
  encryption_configuration {
    encryption_type = "KMS"
    kms_key         = aws_kms_key.ecr_kms_key.arn
  }
}


resource "aws_ecr_lifecycle_policy" "delete_stale_images" {
  repository = aws_ecr_repository.lambda_ecr.name
  policy = jsonencode(
    {
      "rules" : [
        {
          "rulePriority" : 1,
          "description" : "Expire untagged images after 7 days",
          "selection" : {
            "tagStatus" : "untagged",
            "countType" : "sinceImagePushed",
            "countUnit" : "days",
            "countNumber" : 7
          },
          "action" : {
            "type" : "expire"
          }
        }
  ] })
}


output "ecr_repo_url" {
  value = aws_ecr_repository.lambda_ecr.repository_url
}