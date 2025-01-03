resource "aws_apigatewayv2_integration" "oauth" {
  api_id           = var.square_gateway_id
  credentials_arn  = aws_iam_role.gateway_sqs_write.arn
  description      = "oauth redirect URL"
  integration_type = "AWS_PROXY"
  integration_subtype = "SQS-SendMessage"

  request_parameters = {
    "QueueUrl"    = aws_sqs_queue.auth_queue.url
    "Action"      = "oauth"
    "MessageBody" = "$request.body"
  }
}


resource "aws_apigatewayv2_route" "oauth" {
  api_id    = var.square_gateway_id
  route_key = "GET /oauth"
  # authorization_type = "CUSTOM"
  # authorizer_id      = var.square_authorizer_id
  target = "integrations/${aws_apigatewayv2_integration.oauth.id}"
}