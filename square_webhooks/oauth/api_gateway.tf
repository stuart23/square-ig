resource "aws_apigatewayv2_integration" "oauth" {
  api_id              = var.square_gateway_id
  description         = "oauth redirect URL"
  integration_type    = "AWS_PROXY"

  integration_method     = "POST"
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


resource "aws_apigatewayv2_integration_response" "oauth_response" {
  api_id                   = var.square_gateway_id
  integration_id           = aws_apigatewayv2_integration.oauth.id
  integration_response_key = "/302 https://google.com/"
}