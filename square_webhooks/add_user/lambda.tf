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
      square_token_arn            = var.square_token_arn
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


resource "aws_cloudwatch_metric_alarm" "add_user_failure_alarm" {
  alarm_name        = "add_user_failure_alarm"
  alarm_description = "Errors in Lambda Function on add user"
  namespace         = "AWS/Lambda"
  metric_name       = "Errors"
  dimensions = {
    FunctionName = aws_lambda_function.add_user.function_name
  }
  comparison_operator = "GreaterThanThreshold"
  statistic           = "Maximum"
  threshold           = 0
  evaluation_periods  = 1
  period              = 300
  alarm_actions       = [var.alerts_sns_topic_arn]
  ok_actions          = [var.alerts_sns_topic_arn]
}