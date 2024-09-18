# Configure docker provider
provider "docker" {
  registry_auth {
    address  = data.aws_ecr_authorization_token.token.proxy_endpoint
    username = data.aws_ecr_authorization_token.token.user_name
    password = data.aws_ecr_authorization_token.token.password
  }
}

# Build square ig webhook runner image
resource "docker_image" "square_ig_webhook_local" {
  name = aws_ecr_repository.lambda_ecr.repository_url
  build {
    context = "image/."
  }
  platform = "linux/arm64"
  triggers = {
    dir_sha1 = sha1(join("", [filesha1("Dockerfile"), filesha1("lambda_function.sh")]))
  }
}

# Push image to ecr repo
resource "docker_registry_image" "square_ig_webhook_ecr" {
  name     = docker_image.square_ig_webhook_local.name
  triggers = { image_digest = docker_image.square_ig_webhook_local.repo_digest }
}