resource "aws_cloudwatch_log_group" "catalog_update_lambda_logs" {
  name              = "catalog_update_lambda"
  retention_in_days = 14
}

resource "aws_lambda_function" "catalog_update" {
  function_name = "catalog_update"
  description   = "Triggered when the catalog updates. Updates the Dynamo table with the items."
  package_type  = "Image"
  architectures = ["arm64"]
  image_uri     = var.lambda_image
  role          = var.lambda_role_arn
  timeout       = 30
  memory_size   = 256
  image_config {
    command = ["catalog_update.handler"]
  }
  logging_config {
    log_group  = aws_cloudwatch_log_group.catalog_update_lambda_logs.name
    log_format = "Text"
  }
  environment {
    variables = {
      sns_topic_arn    = var.generate_barcode_sns_topic_arn
      square_token_arn = var.square_token_arn
    }
  }
  ephemeral_storage {
    size = 1024 # Min 512 MB and the Max 10240 MB
  }
}


resource "aws_lambda_permission" "catalog_update_permission" {
  statement_id  = "AllowAPIInvoke"
  action        = "lambda:InvokeFunction"
  function_name = "catalog_update"
  principal     = "apigateway.amazonaws.com"

  # The /* part allows invocation from any stage, method and resource path
  # within API Gateway.
  source_arn = "${var.square_gateway_execution_arn}/*"
}


resource "aws_cloudwatch_metric_alarm" "catalog_update_failure_alarm" {
  alarm_name        = "catalog_update_failure_alarm"
  alarm_description = "Errors in Lambda Function on catalog updates"
  namespace         = "AWS/Lambda"
  metric_name       = "Errors"
  dimensions = {
    FunctionName = aws_lambda_function.catalog_update.function_name
  }
  comparison_operator = "GreaterThanThreshold"
  statistic           = "Maximum"
  threshold           = 0
  evaluation_periods  = 1
  period              = 300
  alarm_actions       = [var.alerts_sns_topic_arn]
  ok_actions          = [var.alerts_sns_topic_arn]
}