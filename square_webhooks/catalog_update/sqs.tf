resource "aws_sqs_queue" "catalog_update" {
  name = "catalog_update"
}


resource "aws_iam_policy" "sqs_write" {
  name        = "sqs_write"
  description = "Write to sqs queue"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action   = "sqs:SendMessage"
        Effect   = "Allow"
        Resource = aws_sqs_queue.catalog_update.arn
      },
    ]
  })
}


resource "aws_iam_role" "gateway_sqs_write" {
  name = "sqs_write"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "apigateway.amazonaws.com"
        }
      },
    ]
  })
}


resource "aws_iam_role_policy_attachment" "gateway_sqs_write" {
  role       = aws_iam_role.gateway_sqs_write.name
  policy_arn = aws_iam_policy.sqs_write.arn
}