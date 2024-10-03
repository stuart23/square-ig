resource "aws_cloudwatch_log_group" "api_authorizer_logs" {
  name              = "api_authorizer"
  retention_in_days = 3
}


resource "aws_lambda_function" "api_authorizer" {
  function_name = "api_authorizer"
  description   = "Checks the IP address comes from square"
  package_type  = "Image"
  architectures = ["arm64"]
  image_uri     = var.lambda_image
  role          = aws_iam_role.api_authorizer_role.arn
  timeout       = 5
  image_config {
    command = ["check_ip.handler"]
  }
  logging_config {
    log_group  = aws_cloudwatch_log_group.api_authorizer_logs.name
    log_format = "Text"
  }
}


resource "aws_apigatewayv2_authorizer" "square_webhooks_gateway_authorizer" {
  name                              = "api_authorizer"
  api_id                            = aws_apigatewayv2_api.square_webhooks_gateway.id
  authorizer_type                   = "REQUEST"
  authorizer_uri                    = aws_lambda_function.api_authorizer.invoke_arn
  # identity_sources                  = ["$request.header.Authorization"]
  enable_simple_responses           = true
  authorizer_payload_format_version = "2.0"
}
