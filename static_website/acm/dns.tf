resource "porkbun_dns_record" "main" {
  name    = var.domain_name
  domain  = var.domain_name
  content = "abcdefg"
  type    = "CNAME"
}