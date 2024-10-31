module "add_user" {
  source                       = "./add_user"
  lambda_image                 = var.lambda_image
  square_gateway_id            = aws_apigatewayv2_api.square_webhooks_gateway.id
  square_gateway_execution_arn = aws_apigatewayv2_api.square_webhooks_gateway.execution_arn
  square_authorizer_id         = aws_apigatewayv2_authorizer.square_webhooks_gateway_authorizer.id
  lambda_role_arn              = aws_iam_role.lambda_role.arn
  square_token_arn             = aws_secretsmanager_secret.square_token.arn
  alerts_sns_topic_arn         = module.alerts.alerts_sns_topic_arn
}


module "catalog_update" {
  source                         = "./catalog_update"
  lambda_image                   = var.lambda_image
  instructions_git_repo          = var.instructions_git_repo
  gh_key_arn                     = var.gh_key_arn
  square_gateway_id              = aws_apigatewayv2_api.square_webhooks_gateway.id
  square_gateway_execution_arn   = aws_apigatewayv2_api.square_webhooks_gateway.execution_arn
  square_authorizer_id           = aws_apigatewayv2_authorizer.square_webhooks_gateway_authorizer.id
  lambda_role_arn                = aws_iam_role.lambda_role.arn
  generate_label_sns_topic_arn = module.generate_label.generate_label_sns_topic_arn
  square_token_arn               = aws_secretsmanager_secret.square_token.arn
  alerts_sns_topic_arn           = module.alerts.alerts_sns_topic_arn
}


module "generate_label" {
  source               = "./generate_label"
  lambda_image         = var.lambda_image
  lambda_role_arn      = aws_iam_role.lambda_role.arn
  square_token_arn     = aws_secretsmanager_secret.square_token.arn
  alerts_sns_topic_arn = module.alerts.alerts_sns_topic_arn
}


module "alerts" {
  source = "./alerts"
}