resource "aws_apigatewayv2_integration" "oauth" {
  api_id              = var.square_gateway_id
  description         = "oauth redirect URL"
  integration_type    = "AWS_PROXY"
}

resource "aws_apigatewayv2_route" "oauth" {
  api_id    = var.square_gateway_id
  route_key = "POST /oauth"
  # authorization_type = "CUSTOM"
  # authorizer_id      = var.square_authorizer_id
  target = "integrations/${aws_apigatewayv2_integration.oauth.id}"
}