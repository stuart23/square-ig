resource "aws_dynamodb_table" "tenants" {
  name         = "${var.env_prefix}_tenants"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "oauth_code"

  attribute {
    name = "oauth_code"
    type = "S"
  }
}


# IAM policy for interacting with Dynamo table
resource "aws_iam_policy" "tenants_read_write_policy" {
  name        = "${var.env_prefix}_tenants_read_write_access"
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
          "${aws_dynamodb_table.tenants.arn}/*",
          aws_dynamodb_table.tenants.arn
        ]
      },
    ]
  })
}