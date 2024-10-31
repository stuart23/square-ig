resource "aws_acm_certificate" "certificate" {
  domain_name       = var.domain_name
  validation_method = "DNS"

  lifecycle {
    create_before_destroy = true
  }
}

# # Sleep for a minute to wait for dns records
resource "time_sleep" "wait_5_mins" {
  depends_on      = [porkbun_dns_record.certificate_validation]
  triggers        = { dns_record_id = porkbun_dns_record.certificate_validation[var.domain_name].id }
  create_duration = "5m"
}


resource "aws_acm_certificate_validation" "certificate_validation" {
  depends_on              = [time_sleep.wait_5_mins]
  certificate_arn         = aws_acm_certificate.certificate.arn
}

output "fqdns" {
  value = [for record in porkbun_dns_record.certificate_validation : record.domain]
}

output "certificate_arn" {
  value = aws_acm_certificate.certificate.arn
}

output "certificate_validation" {
  value = aws_acm_certificate_validation.certificate_validation.id
}