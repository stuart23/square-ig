resource "aws_secretsmanager_secret" "square_token" {
  name = "square_token"
}


resource "aws_secretsmanager_secret_version" "square_token_version" {
  secret_id     = aws_secretsmanager_secret.square_token.id
  secret_string = var.square_token
}