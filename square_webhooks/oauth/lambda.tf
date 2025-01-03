resource "aws_cloudwatch_log_group" "oauth" {
  name              = "${var.env_prefix}_oauth"
  retention_in_days = 14
}

resource "aws_lambda_function" "oauth" {
  function_name = "${var.env_prefix}_oauth"
  description                    = "Triggered by square API oauth flow."
  package_type                   = "Image"
  architectures                  = ["arm64"]
  image_uri                      = var.lambda_image
  role                           = var.lambda_role_arn
  timeout                        = 30
  memory_size                    = 256
  publish                        = true
  image_config {
    command = ["oauth_lambda.handler"]
  }
  logging_config {
    log_group  = aws_cloudwatch_log_group.oauth.name
    log_format = "Text"
  }
  # environment {
  #   variables = {
  #     sns_topic_arn         = var.generate_label_sns_topic_arn
  #   }
  # }
}


resource "aws_lambda_permission" "oauth_permission" {
  statement_id  = "AllowAPIInvoke"
  action        = "lambda:InvokeFunction"
  function_name = "${var.env_prefix}_oauth"
  principal     = "apigateway.amazonaws.com"

  # The /* part allows invocation from any stage, method and resource path
  # within API Gateway.
  source_arn = "${var.square_gateway_execution_arn}/*"
}


resource "aws_cloudwatch_metric_alarm" "oauth_failure_alarm" {
  alarm_name        = "${var.env_prefix}_oauth_failure_alarm"
  alarm_description = "Errors in Lambda Function from square oauth flow"
  namespace         = "AWS/Lambda"
  metric_name       = "Errors"
  dimensions = {
    FunctionName = aws_lambda_function.oauth.function_name
  }
  comparison_operator = "GreaterThanThreshold"
  statistic           = "Maximum"
  threshold           = 0
  evaluation_periods  = 1
  period              = 300
  alarm_actions       = [var.alerts_sns_topic_arn]
  ok_actions          = [var.alerts_sns_topic_arn]
}