module "add_user" {
  source                       = "./add_user"
  lambda_image                 = var.lambda_image
  square_gateway_id            = aws_apigatewayv2_api.square_webhooks_gateway.id
  square_gateway_execution_arn = aws_apigatewayv2_api.square_webhooks_gateway.execution_arn
  square_authorizer_id         = aws_apigatewayv2_authorizer.square_webhooks_gateway_authorizer.id
  lambda_role_arn              = aws_iam_role.lambda_role.arn
  instagram_credentials_arn    = aws_secretsmanager_secret.instagram_credentials.arn
  square_token_arn             = aws_secretsmanager_secret.square_token.arn
}


module "catalog_update" {
  source                         = "./catalog_update"
  lambda_image                   = var.lambda_image
  square_gateway_id              = aws_apigatewayv2_api.square_webhooks_gateway.id
  square_gateway_execution_arn   = aws_apigatewayv2_api.square_webhooks_gateway.execution_arn
  square_authorizer_id           = aws_apigatewayv2_authorizer.square_webhooks_gateway_authorizer.id
  lambda_role_arn                = aws_iam_role.lambda_role.arn
  generate_barcode_sns_topic_arn = module.generate_barcode.generate_barcode_sns_topic_arn
  square_token_arn               = aws_secretsmanager_secret.square_token.arn
}


module "generate_barcode" {
  source               = "./generate_barcode"
  lambda_image         = var.lambda_image
  lambda_role_arn      = aws_iam_role.lambda_role.arn
  square_token_arn     = aws_secretsmanager_secret.square_token.arn
  alerts_sns_topic_arn = aws_sns_topic.alerts.arn
}


module "alerts" {
  source          = "./alerts"
  pagerduty_email = var.pagerduty_email
}