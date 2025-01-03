module "catalog_update" {
  source                       = "./catalog_update"
  lambda_image                 = var.lambda_image
  square_gateway_id            = aws_apigatewayv2_api.square_webhooks_gateway.id
  square_gateway_execution_arn = aws_apigatewayv2_api.square_webhooks_gateway.execution_arn
  # square_authorizer_id         = aws_apigatewayv2_authorizer.square_webhooks_gateway_authorizer.id
  lambda_role_arn              = aws_iam_role.lambda_role.arn
  generate_label_sns_topic_arn = module.generate_label.generate_label_sns_topic_arn
  alerts_sns_topic_arn         = module.alerts.alerts_sns_topic_arn
  env_prefix                   = var.env_prefix
}


module "oauth" {
  source                       = "./oauth"
  lambda_image                 = var.lambda_image
  square_gateway_id            = aws_apigatewayv2_api.square_webhooks_gateway.id
  square_gateway_execution_arn = aws_apigatewayv2_api.square_webhooks_gateway.execution_arn
  tenants_table                = aws_dynamodb_table.tenants.name
  lambda_role_arn              = aws_iam_role.lambda_role.arn
  alerts_sns_topic_arn         = module.alerts.alerts_sns_topic_arn
  env_prefix                   = var.env_prefix
}


module "generate_label" {
  source               = "./generate_label"
  lambda_image         = var.lambda_image
  lambda_role_arn      = aws_iam_role.lambda_role.arn
  alerts_sns_topic_arn = module.alerts.alerts_sns_topic_arn
  env_prefix           = var.env_prefix
}


module "alerts" {
  source     = "./alerts"
  env_prefix = var.env_prefix
}