resource "aws_cloudwatch_log_group" "generate_label" {
  name              = "generate_label"
  retention_in_days = 14
}

resource "aws_lambda_function" "generate_label" {
  function_name = "generate_label"
  description   = "Generates a label and saves it in S3"
  package_type  = "Image"
  architectures = ["arm64"]
  image_uri     = var.lambda_image
  role          = var.lambda_role_arn
  timeout       = 30
  memory_size   = 1024
  image_config {
    command = ["generate_label_lambda.handler"]
  }
  logging_config {
    log_group  = aws_cloudwatch_log_group.generate_label.name
    log_format = "Text"
  }
  environment {
    variables = {
      catalog_bucket_name    = aws_s3_bucket.label_bucket.id
      square_token_arn       = var.square_token_arn
      labels_google_drive_id = var.labels_google_drive_id
    }
  }
  ephemeral_storage {
    size = 1024 # Min 512 MB and the Max 10240 MB
  }
}


resource "aws_lambda_permission" "generate_label_permission" {
  statement_id  = "AllowExecutionFromSNS"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.generate_label.function_name
  principal     = "sns.amazonaws.com"
  source_arn    = aws_sns_topic.generate_label.arn
}


resource "aws_cloudwatch_metric_alarm" "generate_label_failure_alarm" {
  alarm_name        = "generate_label_failure_alarm"
  alarm_description = "Errors in Lambda Function on label generation"
  namespace         = "AWS/Lambda"
  metric_name       = "Errors"
  dimensions = {
    FunctionName = aws_lambda_function.generate_label.function_name
  }
  comparison_operator = "GreaterThanThreshold"
  statistic           = "Maximum"
  threshold           = 0
  evaluation_periods  = 1
  period              = 300
  alarm_actions       = [var.alerts_sns_topic_arn]
  ok_actions          = [var.alerts_sns_topic_arn]
}