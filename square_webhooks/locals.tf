locals {
  lambda_logging_format = jsonencode({
    requestId        = "$context.requestId"
    requestTime      = "$context.requestTime"
    requestTimeEpoch = "$context.requestTimeEpoch"
    path             = "$context.path"
    method           = "$context.httpMethod"
    status           = "$context.status"
    responseLength   = "$context.responseLength"
  })

  lambda_assume_role_policy = jsonencode({
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