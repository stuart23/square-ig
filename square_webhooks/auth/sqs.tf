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


resource "aws_iam_role_policy_attachment" "auth_queue_sqs_write" {
  role       = var.lambda_role_arn
  policy_arn = aws_iam_policy.auth_queue_sqs_write.arn
}


resource "aws_lambda_event_source_mapping" "trigger_lambda" {
  event_source_arn = aws_sqs_queue.auth_queue.arn
  function_name    = aws_lambda_function.auth_handler.arn
}