resource "porkbun_dns_record" "main" {
    for_each = aws_acm_certificate.certificate.domain_validation_options 

    domain  = each.key
    name   = each.value.resource_record_name
    record = each.value.resource_record_value
    type   = each.value.resource_record_type
}