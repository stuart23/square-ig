resource "aws_secretsmanager_secret" "square_token" {
  name = "square_token"
}


resource "aws_secretsmanager_secret_version" "square_token_version" {
  secret_id     = aws_secretsmanager_secret.square_token.id
  secret_string = var.square_token
}


resource "aws_secretsmanager_secret" "instagram_credentials" {
  name = "instagram_credentials"
}


resource "aws_secretsmanager_secret_version" "instagram_credentials_version" {
  secret_id = aws_secretsmanager_secret.instagram_credentials.id
  secret_string = jsonencode({
    username = var.instagram_username
    password = var.instagram_password
  })
}