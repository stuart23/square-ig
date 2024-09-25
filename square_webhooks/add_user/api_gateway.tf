resource "aws_apigatewayv2_integration" "add_instagram_user" {
  api_id           = var.square_gateway_id
  integration_type = "AWS_PROXY"

  description            = "Webhook for adding user in Square"
  integration_method     = "POST"
  integration_uri        = aws_lambda_function.add_user.invoke_arn
  payload_format_version = "2.0"
}


resource "aws_apigatewayv2_route" "add_instagram_user" {
  api_id    = var.square_gateway_id
  route_key = "$default"
  authorization_type = "CUSTOM"
  authorizer_id = var.square_authorizer_id
  target = "integrations/${aws_apigatewayv2_integration.add_instagram_user.id}"
}


resource "aws_apigatewayv2_stage" "add_instagram_user" {
  api_id      = var.square_gateway_id
  name        = "add_instagram_user"
  description = "Stage for AddInstagramUser Webhook with logging."
  auto_deploy = true
  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.add_user_gateway_logs.arn
    format          = var.lambda_logging_format
  }
}

resource "aws_cloudwatch_log_group" "add_user_gateway_logs" {
  name              = "square_gateway_add_user"
  retention_in_days = 14
}