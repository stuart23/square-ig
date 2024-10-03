resource "aws_cloudwatch_log_group" "generate_barcode" {
  name              = "generate_barcode"
  retention_in_days = 14
}

resource "aws_lambda_function" "generate_barcode" {
  function_name = "generate_barcode"
  description   = "Generates a barcode, saves it in S3 and updates the dynamo database"
  package_type  = "Image"
  architectures = ["arm64"]
  image_uri     = var.lambda_image
  role          = var.lambda_role_arn
  timeout       = 30
  memory_size   = 256
  image_config {
    command = ["generate_barcode.handler"]
  }
  logging_config {
    log_group  = aws_cloudwatch_log_group.generate_barcode.name
    log_format = "Text"
  }
  environment {
    variables = {
      catalog_bucket_name = aws_s3_bucket.barcode_bucket.id
      square_token_arn    = var.square_token_arn
    }
  }
  ephemeral_storage {
    size = 1024 # Min 512 MB and the Max 10240 MB
  }
}


resource "aws_lambda_permission" "generate_barcode_permission" {
  statement_id  = "AllowExecutionFromSNS"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.generate_barcode.function_name
  principal     = "sns.amazonaws.com"
  source_arn    = aws_sns_topic.generate_barcode.arn
}