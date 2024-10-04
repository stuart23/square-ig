variable "pagerduty_email" {
  description = "Email of existing user in PagerDuty who will receive alerts"
  type        = string
  sensitive   = true
}