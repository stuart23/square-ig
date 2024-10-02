resource "aws_dynamodb_table" "catalog" {
  name           = "catalog"
  billing_mode   = "PROVISIONED"
  read_capacity  = 25
  write_capacity = 25
  hash_key       = "SKU"

  attribute {
    name = "SKU"
    type = "S"
  }
}