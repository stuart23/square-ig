resource "aws_sqs_queue" "auth_queue" {
  name = "${var.env_prefix}_auth"
}


resource "aws_iam_policy" "auth_queue_sqs_write" {
  name        = "${var.env_prefix}_auth_sqs_write"
  description = "Write to sqs queue"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action   = "sqs:SendMessage"
        Effect   = "Allow"
        Resource = aws_sqs_queue.auth_queue.arn
      },
    ]
  })
}


resource "aws_iam_policy" "auth_queue_sqs_read_write" {
  name        = "${var.env_prefix}_auth_sqs_write"
  description = "Write to sqs queue"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "sqs:SendMessage",
          "sqs:ReceiveMessage"
        ]
        Effect   = "Allow"
        Resource = aws_sqs_queue.auth_queue.arn
      },
    ]
  })
}


resource "aws_lambda_event_source_mapping" "trigger_lambda" {
  event_source_arn = aws_sqs_queue.auth_queue.arn
  function_name    = aws_lambda_function.auth_handler.arn
}


resource "aws_cloudwatch_metric_alarm" "auth_sqs_queue_alarm" {
  alarm_name        = "${var.env_prefix}_auth_sqs_queue_alarm"
  alarm_description = "Auth SQS Queue has messages older than 10 seconds."
  namespace         = "AWS/SQS"
  metric_name       = "ApproximateAgeOfOldestMessage"
  dimensions = {
    QueueName = aws_sqs_queue.auth_queue.name
  }
  comparison_operator = "GreaterThanThreshold"
  statistic           = "Maximum"
  threshold           = 10
  evaluation_periods  = 1
  period              = 300
  alarm_actions       = [var.alerts_sns_topic_arn]
  ok_actions          = [var.alerts_sns_topic_arn]
}