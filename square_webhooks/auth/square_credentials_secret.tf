
# The secret is not managed by terraform - it must exist in AWS already.
# It should probably be parameterized rather than hard coded.
data "aws_secretsmanager_secret" "square_credentials" {
  arn = "arn:aws:secretsmanager:us-east-1:015140017687:secret:square_qr_codes_credentials-RJAEmW"
}


resource "aws_iam_policy" "read_square_credentials_secret" {
  name        = "${var.env_prefix}_read_square_credentials_secret"
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
        Resource = aws_secretsmanager_secret.square_credentials.arn
      },
    ]
  })
}