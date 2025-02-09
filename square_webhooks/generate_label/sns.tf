
resource "aws_sns_topic" "generate_label" {
  name = "${var.env_prefix}_generate_label"
}


resource "aws_sns_topic_subscription" "generate_label" {
  topic_arn = aws_sns_topic.generate_label.arn
  protocol  = "lambda"
  endpoint  = aws_lambda_function.generate_label.arn
}


resource "aws_iam_policy" "generate_label_sns_publish" {
  name        = "${var.env_prefix}_generate_label_sns_publish"
  description = "Publish to generate labels sns queue"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action   = "sns:Publish"
        Effect   = "Allow"
        Resource = aws_sns_topic.generate_label.arn
      },
    ]
  })
}


output "generate_label_sns_topic_arn" {
  value = aws_sns_topic.generate_label.arn
}


output "generate_label_sns_publish_policy_arn" {
  value = aws_iam_policy.generate_label_sns_publish.arn
}