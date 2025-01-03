resource "aws_apigatewayv2_integration" "catalog_update_sqs" {
  api_id              = var.square_gateway_id
  credentials_arn     = aws_iam_role.gateway_sqs_write.arn
  description         = "SQS for messages to update catalog"
  integration_type    = "AWS_PROXY"
  integration_subtype = "SQS-SendMessage"

  request_parameters = {
    "QueueUrl"    = aws_sqs_queue.catalog_update.url
    "MessageBody" = "$request.body"
  }
}

resource "aws_apigatewayv2_route" "catalog_update_sqs" {
  api_id    = var.square_gateway_id
  route_key = "POST /catalog_update"
  # authorization_type = "CUSTOM"
  # authorizer_id      = var.square_authorizer_id
  target = "integrations/${aws_apigatewayv2_integration.catalog_update_sqs.id}"
}