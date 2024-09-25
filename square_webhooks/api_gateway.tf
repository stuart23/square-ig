resource "aws_apigatewayv2_api" "square_gateway" {
  name          = "square-http-api"
  description   = "Endpoint for Square webhooks."
  protocol_type = "HTTP"
}

output "gateway_endpoint" {
  value = aws_apigatewayv2_api.square_gateway.api_endpoint
  description = "Endpoint of the square gateway API. Individual endpoints (e.g. /add_user) are appended to this."
}