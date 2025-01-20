resource "aws_cloudwatch_log_group" "webhooks_management" {
  name              = "${var.env_prefix}_webhooks_management_lambda"
  retention_in_days = 14
}


resource "aws_iam_role" "webhooks_management" {
  name               = "${var.env_prefix}_webhooks_management"
  assume_role_policy = local.lambda_assume_role_policy
}

resource "aws_iam_role_policy_attachment" "webhooks_management_read_square_token_secret_attachment" {
  role       = aws_iam_role.webhooks_management.name
  policy_arn = aws_iam_policy.read_square_token_secret.arn
}


resource "aws_iam_role_policy_attachment" "webhooks_management_handler_execute_policy_attachment" {
  role       = aws_iam_role.webhooks_management.name
  policy_arn = "arn:aws:iam::aws:policy/AWSLambdaExecute"
}


resource "aws_lambda_function" "webhooks_management_handler" {
  function_name = "${var.env_prefix}_webhooks_management"
  description   = "webhooks management function"
  package_type  = "Image"
  architectures = ["arm64"]
  image_uri     = var.lambda_image
  role          = aws_iam_role.webhooks_management.arn
  timeout       = 5
  publish       = true
  image_config {
    command = ["webhooks_management_handler_lambda.handler"]
  }
  logging_config {
    log_group  = aws_cloudwatch_log_group.webhooks_management.name
    log_format = "Text"
  }
  environment {
    variables = {
      square_qr_codes_token_arn = data.aws_secretsmanager_secret.square_token.arn
      catalog_update_endpoint   = var.catalog_update_endpoint
      env_prefix                = var.env_prefix
    }
  }
}


# resource "aws_lambda_permission" "auth_handler_permission" {
#   statement_id  = "AllowAPIInvoke"
#   action        = "lambda:InvokeFunction"
#   function_name = aws_lambda_function.auth_handler.function_name
#   principal     = "sqs.amazonaws.com"
#   source_arn    = aws_sqs_queue.auth_queue.arn
# }


resource "aws_cloudwatch_metric_alarm" "webhooks_management_handler_failure_alarm" {
  alarm_name        = "${var.env_prefix}_webhooks_management_handler_failure_alarm"
  alarm_description = "Errors in Lambda Function that turns on the webhooks"
  namespace         = "AWS/Lambda"
  metric_name       = "Errors"
  dimensions = {
    FunctionName = aws_lambda_function.webhooks_management_handler.function_name
  }
  comparison_operator = "GreaterThanThreshold"
  statistic           = "Maximum"
  threshold           = 0
  evaluation_periods  = 1
  period              = 300
  alarm_actions       = [var.alerts_sns_topic_arn]
  ok_actions          = [var.alerts_sns_topic_arn]
}