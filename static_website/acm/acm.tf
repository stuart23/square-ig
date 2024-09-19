resource "aws_acm_certificate" "certificate" {
  domain_name       = var.domain_name
  validation_method = "DNS"

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_acm_certificate_validation" "certificate_validation" {
  certificate_arn = aws_acm_certificate.certificate.arn
  # validation_record_fqdns = [for record in aws_route53_record.example : record.fqdn]
}

output "certificate_status" {
  description = "Certificate status"
  value       = aws_acm_certificate.certificate.status
}