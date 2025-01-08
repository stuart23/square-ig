resource "aws_cloudwatch_log_group" "auth_handler" {
  name              = "${var.env_prefix}_auth_handler"
  retention_in_days = 14
}


resource "aws_iam_role" "auth_handler" {
  name               = "${var.env_prefix}_auth_handler"
  assume_role_policy = local.lambda_assume_role_policy
}


resource "aws_iam_role_policy_attachment" "auth_handler_sqs_read_write_attachment" {
  role       = aws_iam_role.auth_handler.name
  policy_arn = aws_iam_policy.auth_queue_sqs_read_write.arn
}


resource "aws_iam_role_policy_attachment" "auth_handler_execute_policy_attachment" {
  role       = aws_iam_role.auth_handler.name
  policy_arn = "arn:aws:iam::aws:policy/AWSLambdaExecute"
}


resource "aws_iam_role_policy_attachment" "auth_handler_tenants_access_policy_attachment" {
  role       = aws_iam_role.auth_handler.name
  policy_arn = var.tenants_access_policy_arn
}


resource "aws_iam_role_policy_attachment" "auth_handler_secret_access_policy_attachment" {
  role       = aws_iam_role.auth_handler.name
  policy_arn = aws_iam_policy.read_square_credentials_secret.arn
}

resource "aws_lambda_function" "auth_handler" {
  function_name = "${var.env_prefix}_auth_handler"
  description   = "oAuth callback function"
  package_type  = "Image"
  architectures = ["arm64"]
  image_uri     = var.lambda_image
  role          = aws_iam_role.auth_handler.arn
  timeout       = 5
  publish       = true
  image_config {
    command = ["auth_handler_lambda.handler"]
  }
  logging_config {
    log_group  = aws_cloudwatch_log_group.auth_handler.name
    log_format = "Text"
  }
  environment {
    variables = {
      tenants_table_name              = var.tenants_table
      square_qr_codes_credentials_arn = data.aws_secretsmanager_secret.square_credentials.arn
    }
  }
}


resource "aws_lambda_permission" "auth_handler_permission" {
  statement_id  = "AllowAPIInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.auth_handler.function_name
  principal     = "sqs.amazonaws.com"
  source_arn    = aws_sqs_queue.auth_queue.arn
}


resource "aws_cloudwatch_metric_alarm" "auth_handler_failure_alarm" {
  alarm_name        = "${var.env_prefix}_auth_handler_failure_alarm"
  alarm_description = "Errors in Lambda Function from square oauth flow"
  namespace         = "AWS/Lambda"
  metric_name       = "Errors"
  dimensions = {
    FunctionName = aws_lambda_function.auth_handler.function_name
  }
  comparison_operator = "GreaterThanThreshold"
  statistic           = "Maximum"
  threshold           = 0
  evaluation_periods  = 1
  period              = 300
  alarm_actions       = [var.alerts_sns_topic_arn]
  ok_actions          = [var.alerts_sns_topic_arn]
}