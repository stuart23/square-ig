resource "aws_cloudwatch_log_group" "catalog_update_lambda_logs" {
  name              = "${var.env_prefix}_catalog_update_lambda"
  retention_in_days = 14
}


resource "aws_iam_role" "catalog_update" {
  name               = "${var.env_prefix}_catalog_update"
  assume_role_policy = local.lambda_assume_role_policy
}

resource "aws_iam_role_policy_attachment" "catalog_update_sqs_read_write_attachment" {
  role       = aws_iam_role.catalog_update.name
  policy_arn = aws_iam_policy.catalog_update_sqs_read_write.arn
}

resource "aws_iam_role_policy_attachment" "tenants_read_only_attachment" {
  role       = aws_iam_role.catalog_update.name
  policy_arn = var.tenants_read_only_policy_arn
}

resource "aws_iam_role_policy_attachment" "catalog_read_write_attachment" {
  role       = aws_iam_role.catalog_update.name
  policy_arn = var.catalog_read_write_policy_arn
}

resource "aws_iam_role_policy_attachment" "catalog_update_execute_policy_attachment" {
  role       = aws_iam_role.catalog_update.name
  policy_arn = "arn:aws:iam::aws:policy/AWSLambdaExecute"
}


resource "aws_lambda_function" "catalog_update" {
  function_name                  = "${var.env_prefix}_catalog_update"
  description                    = "Triggered when the catalog updates. Updates the Dynamo table with the items."
  package_type                   = "Image"
  architectures                  = ["arm64"]
  reserved_concurrent_executions = 1
  image_uri                      = var.lambda_image
  role                           = aws_iam_role.catalog_update.arn
  timeout                        = 120
  memory_size                    = 256
  publish                        = true
  image_config {
    command = ["catalog_update_lambda.handler"]
  }
  logging_config {
    log_group  = aws_cloudwatch_log_group.catalog_update_lambda_logs.name
    log_format = "Text"
  }
  environment {
    variables = {
      sns_topic_arn      = var.generate_label_sns_topic_arn
      tenants_table_name = var.tenants_table_name
      catalog_table_name = var.catalog_table_name
    }
  }
  ephemeral_storage {
    size = 1024 # Min 512 MB and the Max 10240 MB
  }
}


resource "aws_lambda_permission" "catalog_update_permission" {
  statement_id  = "AllowAPIInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.catalog_update.function_name
  principal     = "sqs.amazonaws.com"
  source_arn    = aws_sqs_queue.catalog_update.arn
}


resource "aws_cloudwatch_metric_alarm" "catalog_update_failure_alarm" {
  alarm_name        = "${var.env_prefix}_catalog_update_failure_alarm"
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