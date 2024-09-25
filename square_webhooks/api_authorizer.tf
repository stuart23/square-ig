

resource "aws_apigatewayv2_authorizer" "square_gateway" {
  api_id                            = aws_apigatewayv2_api.square_gateway.id
  authorizer_type                   = "REQUEST"
  authorizer_uri                    = aws_lambda_function.example.invoke_arn
  identity_sources                  = ["$request.header.Authorization"]
  name                              = "example-authorizer"
  authorizer_payload_format_version = "2.0"
}
