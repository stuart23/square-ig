resource "aws_iam_policy" "write_metrics" {
  name        = "${var.env_prefix}_write_metrics"
  description = "Access to push metrics to cloudwatch"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid = "WriteMetrics"
        Action = [
          "cloudwatch:PutMetricData",
        ]
        Effect   = "Allow"
        Resource = "*"
      }
    ]
  })
}