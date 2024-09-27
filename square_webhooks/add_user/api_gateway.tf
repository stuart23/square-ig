resource "aws_apigatewayv2_integration" "add_instagram_user" {
  api_id           = var.square_gateway_id
  integration_type = "AWS_PROXY"

  description            = "Webhook for adding user in Square"
  integration_method     = "POST"
  integration_uri        = aws_lambda_function.add_user.invoke_arn
  payload_format_version = "2.0"
}


resource "aws_apigatewayv2_route" "add_instagram_user" {
  api_id             = var.square_gateway_id
  route_key          = "POST /add_instagram_user"
  authorization_type = "CUSTOM"
  authorizer_id      = var.square_authorizer_id
  target             = "integrations/${aws_apigatewayv2_integration.add_instagram_user.id}"
}