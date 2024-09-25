module "add_user" {
  source            = "./add_user"
  lambda_image      = var.lambda_image
  square_gateway_id = aws_apigatewayv2_api.square_gateway.id
  lambda_role_arn   = aws_iam_role.lambda_role.arn
}