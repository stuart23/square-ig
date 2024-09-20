resource "aws_cloudwatch_log_group" "add_user_logs" {
  name              = "add_user"
  retention_in_days = 14
}

resource "aws_lambda_function" "add_user" {
  function_name = "add_user"
  description   = "Deploys DAGs in S3 bucket to Astro"
  package_type  = "Image"
  architectures = ["arm64"]
  image_uri     = "015140017687.dkr.ecr.us-east-1.amazonaws.com/lambdaimage@sha256:9372e5dcca5d63b4fd59e6cfe61d223bd1cccf1d408bb3ef06e4b08f916ff29b"
  # image_uri     = var.lambda_image
  role          = aws_iam_role.lambda_role.arn
  timeout       = 30
  memory_size   = 256
  logging_config {
    log_group  = aws_cloudwatch_log_group.add_user_logs.name
    log_format = "Text"
  }
  # environment {
  #   variables = {
  #     token = token
  #   }
  # }
  ephemeral_storage {
    size = 1024 # Min 512 MB and the Max 10240 MB
  }
}