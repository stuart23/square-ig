locals {
  catalog_update_route = "catalog_update"

  lambda_assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      },
    ]
  })
}

output "catalog_update_route" {
  value = local.catalog_update_route
}