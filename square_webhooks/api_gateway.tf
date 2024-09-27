resource "aws_apigatewayv2_api" "square_webhooks_gateway" {
  name          = "square_http_api"
  description   = "Endpoint for Square webhooks."
  protocol_type = "HTTP"
}


resource "aws_apigatewayv2_stage" "square_webhooks_stage" {
  api_id      = aws_apigatewayv2_api.square_gateway.id
  name        = "$default"
  description = "Stage for Square Webhooks with logging."
  auto_deploy = true
  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.square_webhooks_logs.arn
    format          = local.lambda_logging_format
  }
}

resource "aws_cloudwatch_log_group" "square_webhooks_logs" {
  name              = "square_webhooks_logs"
  retention_in_days = 14
}

output "gateway_endpoint" {
  value       = aws_apigatewayv2_api.square_gateway.api_endpoint
  description = "Endpoint of the square gateway API. Individual endpoints (e.g. /add_user) are appended to this."
}