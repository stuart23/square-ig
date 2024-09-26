module "add_user" {
  source                       = "./add_user"
  lambda_image                 = var.lambda_image
  square_gateway_id            = aws_apigatewayv2_api.square_gateway.id
  square_gateway_execution_arn = aws_apigatewayv2_api.square_gateway.execution_arn
  square_authorizer_id         = aws_apigatewayv2_authorizer.square_gateway.id
  lambda_role_arn              = aws_iam_role.lambda_role.arn
  lambda_logging_format        = local.lambda_logging_format
}


module "catalog_update" {
  source                       = "./catalog_update"
  lambda_image                 = var.lambda_image
  square_gateway_id            = aws_apigatewayv2_api.square_gateway.id
  square_gateway_execution_arn = aws_apigatewayv2_api.square_gateway.execution_arn
  square_authorizer_id         = aws_apigatewayv2_authorizer.square_gateway.id
  lambda_role_arn              = aws_iam_role.lambda_role.arn
  lambda_logging_format        = local.lambda_logging_format

}