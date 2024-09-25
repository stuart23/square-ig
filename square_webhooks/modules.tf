module "acm" {
  source             = "./add_user"
  lambda_image        = var.lambda_image
}