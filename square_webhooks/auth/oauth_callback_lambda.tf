resource "aws_cloudwatch_log_group" "oauth_callback" {
  name              = "${var.env_prefix}_oauth_callback"
  retention_in_days = 14
}

resource "aws_lambda_function" "oauth_callback" {
  function_name = "${var.env_prefix}_oauth_callback"
  description   = "oAuth callback function"
  package_type  = "Image"
  architectures = ["arm64"]
  image_uri     = var.lambda_image
  role          = var.lambda_role_arn
  timeout       = 30
  memory_size   = 256
  publish       = true
  image_config {
    command = ["auth_callback_lambda.handler"]
  }
  logging_config {
    log_group  = aws_cloudwatch_log_group.oauth_callback.name
    log_format = "Text"
  }
}


resource "aws_lambda_permission" "oauth_callback_permission" {
  statement_id  = "AllowAPIInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.oauth_callback.function_name
  principal     = "apigateway.amazonaws.com"

  # The /* part allows invocation from any stage, method and resource path
  # within API Gateway.
  source_arn = "${var.square_gateway_execution_arn}/*"
}


resource "aws_cloudwatch_metric_alarm" "oauth_callback_failure_alarm" {
  alarm_name        = "${var.env_prefix}_auth_failure_alarm"
  alarm_description = "Errors in Lambda Function from square oauth flow"
  namespace         = "AWS/Lambda"
  metric_name       = "Errors"
  dimensions = {
    FunctionName = aws_lambda_function.oauth_callback.function_name
  }
  comparison_operator = "GreaterThanThreshold"
  statistic           = "Maximum"
  threshold           = 0
  evaluation_periods  = 1
  period              = 300
  alarm_actions       = [var.alerts_sns_topic_arn]
  ok_actions          = [var.alerts_sns_topic_arn]
}