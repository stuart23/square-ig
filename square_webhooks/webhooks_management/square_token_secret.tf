
# The secret is not managed by terraform - it must exist in AWS already.
# It should probably be parameterized rather than hard coded.
data "aws_secretsmanager_secret" "square_token" {
  arn = "arn:aws:secretsmanager:us-east-1:015140017687:secret:square_qr_codes_token-c8z9un"
}


resource "aws_iam_policy" "read_square_token_secret" {
  name        = "${var.env_prefix}_read_square_token_secret"
  description = "Read square_credentials secret used in lambda function"
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
        Resource = data.aws_secretsmanager_secret.square_token.arn
      },
    ]
  })
}