resource "aws_acm_certificate" "certificate" {
  depends_on = [ porkbun_dns_record.certificate_validation ]
  domain_name       = var.domain_name
  validation_method = "DNS"

  lifecycle {
    create_before_destroy = true
  }
}

# # Sleep for a minute to wait for dns records
# resource "time_sleep" "wait_60_seconds" {
#   depends_on      = [porkbun_dns_record.main]
#   triggers        = { dns_record_id = porkbun_dns_record.main[var.domain_name].id }
#   create_duration = "1m"
# }


# resource "aws_acm_certificate_validation" "certificate_validation" {
#   depends_on              = [time_sleep.wait_60_seconds]
#   certificate_arn         = aws_acm_certificate.certificate.arn
#   validation_record_fqdns = [for record in porkbun_dns_record.main : record.domain]
# }

output "fqdns" {
  value = [for record in porkbun_dns_record.certificate_validation : record.domain]
}

output "certificate_arn" {
  value = aws_acm_certificate.certificate.arn
}