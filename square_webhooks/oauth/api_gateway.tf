resource "aws_apigatewayv2_integration" "oauth" {
  api_id              = var.square_gateway_id
  description         = "oauth redirect URL"
  integration_type    = "HTTP_PROXY"

  integration_method     = "GET"
  integration_uri        = aws_lambda_function.oauth.invoke_arn
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "oauth" {
  api_id    = var.square_gateway_id
  route_key = "GET /oauth"
  # authorization_type = "CUSTOM"
  # authorizer_id      = var.square_authorizer_id
  target = "integrations/${aws_apigatewayv2_integration.oauth.id}"
}