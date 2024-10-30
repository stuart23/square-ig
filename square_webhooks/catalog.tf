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

  attribute {
    name = "website"
    type = "S"
  }

  attribute {
    name = "label"
    type = "S"
  }

  global_secondary_index {
    name               = "websiteIndex"
    hash_key           = "website"
    projection_type    = "ALL"
  }

  global_secondary_index {
    name               = "labelIndex"
    hash_key           = "label"
    projection_type    = "ALL"
  }
}