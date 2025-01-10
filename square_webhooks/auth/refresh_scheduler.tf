resource "aws_scheduler_schedule" "trigger_token_refresh" {
  name = "${var.env_prefix}_trigger_token_refresh"

  flexible_time_window {
    mode = "OFF"
  }

  #   schedule_expression = "rate(6 hours)"
  schedule_expression = "rate(5 minutes)"

  target {
    arn      = aws_sqs_queue.auth_queue.arn
    role_arn = aws_iam_role.trigger_token_refresh.arn
    input = jsonencode({
      action = "find_tokens_to_refresh",
    })
  }
}


resource "aws_iam_role" "trigger_token_refresh" {
  name = "${var.env_prefix}_trigger_token_refresh"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "scheduler.amazonaws.com"
        }
      },
    ]
  })
}


resource "aws_iam_role_policy_attachment" "sqs_write_attachment" {
  role       = aws_iam_role.trigger_token_refresh.name
  policy_arn = aws_iam_policy.auth_queue_sqs_write.arn
}

