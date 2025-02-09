module "catalog_update" {
  source                       = "./catalog_update"
  lambda_image                 = var.lambda_image
  square_gateway_id            = aws_apigatewayv2_api.square_webhooks_gateway.id
  square_gateway_execution_arn = aws_apigatewayv2_api.square_webhooks_gateway.execution_arn
  # square_authorizer_id         = aws_apigatewayv2_authorizer.square_webhooks_gateway_authorizer.id
  tenants_read_only_policy_arn          = aws_iam_policy.tenants_read_only_policy.arn
  tenants_table_name                    = aws_dynamodb_table.tenants.name
  catalog_read_write_policy_arn         = aws_iam_policy.catalog_read_write_policy.arn
  catalog_table_name                    = aws_dynamodb_table.catalog.name
  generate_label_sns_topic_arn          = module.generate_label.generate_label_sns_topic_arn
  generate_label_sns_publish_policy_arn = module.generate_label.generate_label_sns_publish_policy_arn
  alerts_sns_topic_arn                  = module.alerts.alerts_sns_topic_arn
  env_prefix                            = var.env_prefix
  lambda_assume_role_policy             = local.lambda_assume_role_policy
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
  lambda_assume_role_policy    = local.lambda_assume_role_policy
}


module "generate_label" {
  source               = "./generate_label"
  lambda_image         = var.lambda_image
  alerts_sns_topic_arn = module.alerts.alerts_sns_topic_arn
  env_prefix           = var.env_prefix
  lambda_assume_role_policy    = local.lambda_assume_role_policy
  catalog_read_write_policy_arn         = aws_iam_policy.catalog_read_write_policy.arn
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
  lambda_assume_role_policy    = local.lambda_assume_role_policy
}