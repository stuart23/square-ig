resource "aws_sns_topic" "alerts" {
  name = "alerts"
}

resource "aws_sns_topic_subscription" "alerts_sms" {
  topic_arn = aws_sns_topic.alerts.arn
  protocol  = "https"
  endpoint  = "https://google.com"
}


resource "aws_iam_role" "sns_cloudwatch_role" {
  name = "sns_cloudwatch_role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "sns.amazonaws.com"
        }
      }
    ]
  })
}


# IAM policy for publishing to SNS
resource "aws_iam_policy" "sns_cloudwatch_policy" {
  name        = "sns_cloudwatch_policy"
  description = "Write logs to cloudwatch"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents",
          "logs:PutMetricFilter",
          "logs:PutRetentionPolicy"
        ]
        Effect   = "Allow"
        Resource = "*"
      },
    ]
  })
}


resource "aws_iam_role_policy_attachment" "sns_cloudwatch_attachment" {
  role       = aws_iam_role.sns_cloudwatch_role.name
  policy_arn = aws_iam_policy.sns_cloudwatch_policy.arn
}