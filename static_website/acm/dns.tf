resource "porkbun_dns_record" "main" {
  name    = vars.domain_name
  domain  = vars.domain_name
  content = "abcdefg"
  type    = "CNAME"
}