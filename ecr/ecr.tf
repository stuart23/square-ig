terraform {
  required_version = "~> 1.9.5"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  backend "s3" {
    bucket         	   = "square-ig-tfstate"
    key              	   = "state/terraform.tfstate"
    encrypt        	   = true
    dynamodb_table = "square-ig-tfstate"
  }
}

# Configure the AWS Provider
provider "aws" {
}

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

# # IAM policy for retrieving Secrets from SecretsManager
# resource "aws_iam_policy" "read_secret" {
#   name        = "read_secret"
#   description = "Read secrets used in lambda function"
#   policy = jsonencode({
#     Version = "2012-10-17"
#     Statement = [
#       {
#         Action = [
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

# resource "aws_iam_role" "lambda_role" {
#   name = "lambda_role"
#   assume_role_policy = jsonencode({
#     Version = "2012-10-17"
#     Statement = [
#       {
#         Action = "sts:AssumeRole"
#         Effect = "Allow"
#         Principal = {
#           Service = "lambda.amazonaws.com"
#         }
#       },
#     ]
#   })
# }

# resource "aws_iam_role_policy_attachment" "lambda_role_secrets_policy_attachment" {
#   role       = aws_iam_role.lambda_role.name
#   policy_arn = aws_iam_policy.read_secret.arn
# }

# resource "aws_iam_role_policy_attachment" "lambda_role_execute_policy_attachment" {
#   role       = aws_iam_role.lambda_role.name
#   policy_arn = "arn:aws:iam::aws:policy/AWSLambdaExecute"
# }

# resource "aws_cloudwatch_log_group" "deploy_dags_logs" {
#   name              = "deploy_function"
#   retention_in_days = 14
# }

# resource "aws_lambda_function" "deploy_dags_function" {
#   function_name = "deploy_function"
#   description   = "Deploys DAGs in S3 bucket to Astro"
#   package_type  = "Image"
#   architectures = ["arm64"]
#   image_uri     = "${docker_registry_image.deploy_runner_ecr.name}@${docker_registry_image.deploy_runner_ecr.sha256_digest}"
#   role          = aws_iam_role.lambda_role.arn
#   timeout       = 30
#   depends_on    = [docker_registry_image.deploy_runner_ecr]
#   memory_size   = 256
#   logging_config {
#     log_group  = aws_cloudwatch_log_group.deploy_dags_logs.name
#     log_format = "Text"
#   }
#   environment {
#     variables = {
#       astro_api_token_secret_name = var.astro_api_token_secret_name
#     }
#   }
#   ephemeral_storage {
#     size = 1024 # Min 512 MB and the Max 10240 MB
#   }
# }

# # Bucket for storing the DAGs - can be accessed by the lambda role.
# resource "aws_s3_bucket" "dags_bucket" {
#   bucket = "dagsdeploy"
# }

# resource "aws_s3_bucket_policy" "allow_access_from_lambda_role" {
#   bucket = aws_s3_bucket.dags_bucket.id
#   policy = data.aws_iam_policy_document.allow_access_from_lambda_role.json
# }

# data "aws_iam_policy_document" "allow_access_from_lambda_role" {
#   statement {
#     principals {
#       type        = "AWS"
#       identifiers = [aws_iam_role.lambda_role.arn]
#     }

#     actions = [
#       "s3:GetObject",
#       "s3:ListBucket",
#     ]

#     resources = [
#       aws_s3_bucket.dags_bucket.arn,
#       "${aws_s3_bucket.dags_bucket.arn}/*",
#     ]
#   }
# }

# resource "aws_s3_bucket_notification" "dags_bucket_trigger" {
#   bucket     = aws_s3_bucket.dags_bucket.id
#   depends_on = [aws_lambda_permission.invoke_dags_deploy_permissions]

#   lambda_function {
#     lambda_function_arn = aws_lambda_function.deploy_dags_function.arn
#     # The following runs the function on creation and deletion of DAG files.
#     # See the event types here:
#     # https://docs.aws.amazon.com/AmazonS3/latest/userguide/notification-how-to-event-types-and-destinations.html
#     events = [
#       "s3:ObjectCreated:*",
#       "s3:ObjectRemoved:*"
#     ]
#   }
# }

# resource "aws_lambda_permission" "invoke_dags_deploy_permissions" {
#   statement_id  = "AllowS3Invoke"
#   action        = "lambda:InvokeFunction"
#   function_name = aws_lambda_function.deploy_dags_function.arn
#   principal     = "s3.amazonaws.com"
#   source_arn    = aws_s3_bucket.dags_bucket.arn
# }

# output "s3_bucket_name" {
#   value = aws_s3_bucket.dags_bucket.bucket
# }