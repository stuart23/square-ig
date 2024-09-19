resource "aws_acm_certificate" "certificate" {
  domain_name       = "theplantsocietyatx.com"
  validation_method = "DNS"

  lifecycle {
    create_before_destroy = true
  }
}