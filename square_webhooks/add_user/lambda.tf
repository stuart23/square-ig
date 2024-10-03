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
  role          = var.lambda_role_arn
  timeout       = 30
  memory_size   = 256
  image_config {
    command = ["add_user.handler"]
  }
  logging_config {
    log_group  = aws_cloudwatch_log_group.add_user_lambda_logs.name
    log_format = "Text"
  }
  environment {
    variables = {
      instagram_credentials_arn = var.instagram_credentials_arn
    }
  }
  ephemeral_storage {
    size = 1024 # Min 512 MB and the Max 10240 MB
  }
}


resource "aws_lambda_permission" "add_user_permission" {
  statement_id  = "AllowAPIInvoke"
  action        = "lambda:InvokeFunction"
  function_name = "add_user"
  principal     = "apigateway.amazonaws.com"

  # The /* part allows invocation from any stage, method and resource path
  # within API Gateway.
  source_arn = "${var.square_gateway_execution_arn}/*"
}