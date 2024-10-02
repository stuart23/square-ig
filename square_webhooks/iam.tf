# IAM policy for retrieving Secrets from SecretsManager
resource "aws_iam_policy" "read_secret" {
  name        = "read_secret"
  description = "Read secrets used in lambda function"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "secretsmanager:GetSecretValue",
          "secretsmanager:DescribeSecret",
          "secretsmanager:ListSecretVersionIds",
          "secretsmanager:ListSecrets",
          "secretsmanager:BatchGetSecretValue",
        ]
        Effect   = "Allow"
        Resource = "*"
      },
    ]
  })
}


# IAM policy for interacting with Dynamo table
resource "aws_iam_policy" "dynamo_access" {
  name        = "dynamo_access"
  description = "Access DynamoDB table with catalog data"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid = "ListAndDescribe"
        Action = [
          "dynamodb:List*",
          "dynamodb:DescribeReservedCapacity*",
          "dynamodb:DescribeLimits",
          "dynamodb:DescribeTimeToLive"
        ]
        Effect   = "Allow"
        Resource = "*"
      },
      {
        Sid = "AccessCatalog"
        Action = [
          "dynamodb:BatchGet*",
          "dynamodb:DescribeStream",
          "dynamodb:DescribeTable",
          "dynamodb:Get*",
          "dynamodb:Query",
          "dynamodb:Scan",
          "dynamodb:BatchWrite*",
          "dynamodb:CreateTable",
          "dynamodb:Delete*",
          "dynamodb:Update*",
          "dynamodb:PutItem"
        ]
        Effect   = "Allow"
        Resource = aws_dynamodb_table.catalog.arn
      },
    ]
  })
}


resource "aws_iam_role" "lambda_role" {
  name = "lambda_role"
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


resource "aws_iam_role_policy_attachment" "lambda_role_dynamo_access_policy_attachment" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.dynamo_access.arn
}


resource "aws_iam_role_policy_attachment" "lambda_role_secrets_policy_attachment" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.read_secret.arn
}


resource "aws_iam_role_policy_attachment" "lambda_role_execute_policy_attachment" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/AWSLambdaExecute"
}


resource "aws_iam_role" "api_authorizer_role" {
  name = "api_authorizer_role"
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


resource "aws_iam_role_policy_attachment" "api_authorizer_role_execute_policy_attachment" {
  role       = aws_iam_role.api_authorizer_role.name
  policy_arn = "arn:aws:iam::aws:policy/AWSLambdaExecute"
}
