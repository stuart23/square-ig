resource "aws_dynamodb_table" "catalog" {
  name           = "catalog"
  billing_mode   = "PROVISIONED"
  read_capacity  = 10
  write_capacity = 10
  hash_key       = "variation_id"

  attribute {
    name = "variation_id"
    type = "S"
  }

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
    name            = "skuIndex"
    hash_key        = "sku"
    projection_type = "ALL"
    read_capacity   = 2
    write_capacity  = 2
  }

  global_secondary_index {
    name            = "websiteIndex"
    hash_key        = "website"
    projection_type = "ALL"
    read_capacity   = 2
    write_capacity  = 2
  }

  global_secondary_index {
    name            = "labelIndex"
    hash_key        = "label"
    projection_type = "ALL"
    read_capacity   = 2
    write_capacity  = 2
  }
}