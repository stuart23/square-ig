resource "porkbun_dns_record" "main" {
  for_each = {
    for dvo in aws_acm_certificate.certificate.domain_validation_options : dvo.domain_name => {
      name   = dvo.resource_record_name
      record = dvo.resource_record_value
      type   = dvo.resource_record_type
    }
  }

  domain  = each.key
  name    = replace(each.value.name, var.domain_name, "")
  content = each.value.record
  type    = each.value.type
}