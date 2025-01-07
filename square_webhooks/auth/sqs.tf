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


resource "aws_iam_role" "auth_queue_sqs_write" {
  name = "${var.env_prefix}_auth_sqs_write"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      },
    ]
  })
}


resource "aws_iam_role_policy_attachment" "auth_queue_sqs_write" {
  role       = aws_iam_role.auth_queue_sqs_write.name
  policy_arn = aws_iam_policy.auth_queue_sqs_write.arn
}


resource "aws_iam_role_policy_attachment" "auth_queue_execute_policy_attachment" {
  role       = aws_iam_role.auth_queue_sqs_write.name
  policy_arn = "arn:aws:iam::aws:policy/AWSLambdaExecute"
}


resource "aws_lambda_event_source_mapping" "trigger_lambda" {
  event_source_arn = aws_sqs_queue.auth_queue.arn
  function_name    = aws_lambda_function.auth_handler.arn
}