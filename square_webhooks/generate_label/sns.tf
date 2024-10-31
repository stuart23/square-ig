
resource "aws_sns_topic" "generate_label" {
  name = "generate_label"
}


resource "aws_sns_topic_subscription" "generate_label" {
  topic_arn = aws_sns_topic.generate_label.arn
  protocol  = "lambda"
  endpoint  = aws_lambda_function.generate_label.arn
}

output "generate_label_sns_topic_arn" {
  value = aws_sns_topic.generate_label.arn
}