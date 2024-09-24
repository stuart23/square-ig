resource "aws_cloudwatch_log_group" "add_user_lambda_logs" {
  name              = "add_user_lambda"
  retention_in_days = 14
}

resource "aws_lambda_function" "add_user" {
  function_name = "add_user"
  description   = "Deploys DAGs in S3 bucket to Astro"
  package_type  = "Image"
  architectures = ["arm64"]
  image_uri     = var.lambda_image
  role          = aws_iam_role.lambda_role.arn
  timeout       = 30
  memory_size   = 256
  handler       = "add_user.handler"
  logging_config {
    log_group  = aws_cloudwatch_log_group.add_user_lambda_logs.name
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