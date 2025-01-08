resource "aws_apigatewayv2_integration" "oauth_callback" {
  api_id           = var.square_gateway_id
  description      = "Calls auth_callback_lambda to handle oauth callbacks."
  integration_type = "AWS_PROXY"
  integration_uri  = aws_lambda_function.oauth_callback.invoke_arn
}

resource "aws_apigatewayv2_route" "oauth_callback" {
  api_id    = var.square_gateway_id
  route_key = "GET /oauth"
  # authorization_type = "CUSTOM"
  # authorizer_id      = var.square_authorizer_id
  target = "integrations/${aws_apigatewayv2_integration.oauth_callback.id}"
}