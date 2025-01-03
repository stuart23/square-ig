resource "aws_dynamodb_table" "tenants" {
  name           = "${var.env_prefix}_tenants"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "oauth_code"

  attribute {
    name = "oauth_code"
    type = "S"
  }
}