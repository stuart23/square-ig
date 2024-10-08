resource "aws_apigatewayv2_integration" "catalog_update" {
  api_id           = var.square_gateway_id
  integration_type = "AWS_PROXY"

  description            = "Webhook triggered when the catalog is updated"
  integration_method     = "POST"
  integration_uri        = aws_lambda_function.catalog_update.invoke_arn
  payload_format_version = "2.0"
}


resource "aws_apigatewayv2_route" "catalog_update" {
  api_id    = var.square_gateway_id
  route_key = "POST /catalog_update"
  # authorization_type = "CUSTOM"
  # authorizer_id      = var.square_authorizer_id
  target = "integrations/${aws_apigatewayv2_integration.catalog_update.id}"
}


resource "aws_cloudwatch_log_group" "catalog_update_gateway_logs" {
  name              = "catalog_update_gateway_logs"
  retention_in_days = 14
}