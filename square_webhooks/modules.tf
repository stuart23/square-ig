module "catalog_update" {
  source                       = "./catalog_update"
  lambda_image                 = var.lambda_image
  square_gateway_id            = aws_apigatewayv2_api.square_webhooks_gateway.id
  square_gateway_execution_arn = aws_apigatewayv2_api.square_webhooks_gateway.execution_arn
  # square_authorizer_id         = aws_apigatewayv2_authorizer.square_webhooks_gateway_authorizer.id
  tenants_read_only_policy_arn = aws_iam_policy.tenants_read_only_policy.arn
  tenants_table_arn            = aws_dynamodb_table.tenants.arn
  generate_label_sns_topic_arn = module.generate_label.generate_label_sns_topic_arn
  alerts_sns_topic_arn         = module.alerts.alerts_sns_topic_arn
  env_prefix                   = var.env_prefix
}


module "auth" {
  source                       = "./auth"
  lambda_image                 = var.lambda_image
  square_gateway_id            = aws_apigatewayv2_api.square_webhooks_gateway.id
  square_gateway_execution_arn = aws_apigatewayv2_api.square_webhooks_gateway.execution_arn
  tenants_table                = aws_dynamodb_table.tenants.name
  tenants_access_policy_arn    = aws_iam_policy.tenants_read_write_policy.arn
  alerts_sns_topic_arn         = module.alerts.alerts_sns_topic_arn
  env_prefix                   = var.env_prefix
  write_metrics_policy_arn     = aws_iam_policy.write_metrics.arn
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


module "webhooks_management" {
  source                  = "./webhooks_management"
  alerts_sns_topic_arn    = module.alerts.alerts_sns_topic_arn
  lambda_image            = var.lambda_image
  env_prefix              = var.env_prefix
  catalog_update_endpoint = "${aws_apigatewayv2_stage.square_webhooks_stage.invoke_url}${module.catalog_update.catalog_update_route}"
}