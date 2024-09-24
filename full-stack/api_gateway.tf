resource "aws_apigatewayv2_api" "square_gateway" {
  name          = "square-http-api"
  description   = "Endpoint for Square webhooks."
  protocol_type = "HTTP"
}


resource "aws_apigatewayv2_integration" "add_instagram_user" {
  api_id           = aws_apigatewayv2_api.square_gateway.id
  integration_type = "AWS_PROXY"

  description            = "Webhook for adding user in Square"
  integration_method     = "POST"
  integration_uri        = aws_lambda_function.add_user.invoke_arn
  payload_format_version = "2.0"
}


resource "aws_apigatewayv2_route" "add_instagram_user" {
  api_id    = aws_apigatewayv2_api.square_gateway.id
  route_key = "$default"

  target = "integrations/${aws_apigatewayv2_integration.add_instagram_user.id}"
}


resource "aws_apigatewayv2_stage" "add_instagram_user" {
  api_id      = aws_apigatewayv2_api.square_gateway.id
  name        = "add_instagram_user"
  description = "Stage for AddInstagramUser Webhook with logging."
  auto_deploy = true
  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.add_user_gateway_logs.arn
    format = jsonencode({
      requestId        = "$context.requestId"
      requestTime      = "$context.requestTime"
      requestTimeEpoch = "$context.requestTimeEpoch"
      path             = "$context.path"
      method           = "$context.httpMethod"
      status           = "$context.status"
      responseLength   = "$context.responseLength"
    })
  }
}

resource "aws_cloudwatch_log_group" "add_user_gateway_logs" {
  name              = "square_gateway_add_user"
  retention_in_days = 14
}
