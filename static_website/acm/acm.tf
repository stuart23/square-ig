resource "aws_acm_certificate" "certificate" {
  domain_name       = var.domain_name
  validation_method = "DNS"

  lifecycle {
    create_before_destroy = true
  }
}

# Sleep for a minute to wait for dns records
resource "time_sleep" "wait_30_seconds" {
  depends_on = [porkbun_dns_record.main]

  create_duration = "1m"
}


resource "aws_acm_certificate_validation" "certificate_validation" {
  depends_on = [time_sleep.wait_30_seconds]
  certificate_arn = aws_acm_certificate.certificate.arn
  validation_record_fqdns = [for record in porkbun_dns_record.main : record.domain]
}

output "fqdns" {
  value = [for record in porkbun_dns_record.main : record.domain]
}