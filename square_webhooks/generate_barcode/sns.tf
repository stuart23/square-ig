
resource "aws_sns_topic" "generate_barcode" {
  name = "generate_barcode"
}


resource "aws_sns_topic_subscription" "generate_barcode" {
  topic_arn = aws_sns_topic.generate_barcode.arn
  protocol  = "lambda"
  endpoint  = aws_lambda_function.generate_barcode.arn
}

output "generate_barcode_sns_topic_arn" {
  value = aws_sns_topic.generate_barcode.arn
}