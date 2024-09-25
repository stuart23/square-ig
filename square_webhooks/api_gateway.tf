resource "aws_apigatewayv2_api" "square_gateway" {
  name          = "square-http-api"
  description   = "Endpoint for Square webhooks."
  protocol_type = "HTTP"
}