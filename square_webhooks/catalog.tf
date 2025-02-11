resource "aws_dynamodb_table" "catalog" {
  name           = "${var.env_prefix}_catalog"
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
    hash_key        = "SKU"
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


# IAM policy for interacting with Dynamo table
resource "aws_iam_policy" "catalog_read_write_policy" {
  name        = "${var.env_prefix}_catalog_read_write_access"
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
        Sid = "AccessTables"
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
        Effect = "Allow"
        Resource = [
          "${aws_dynamodb_table.catalog.arn}/*",
          aws_dynamodb_table.catalog.arn
        ]
      },
    ]
  })
}