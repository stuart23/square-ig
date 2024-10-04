variable "pagerduty_api_key" {
  description = "API key needed for sending alerts to PagerDuty"
  type        = string
  sensitive   = true
}


variable "pagerduty_email" {
  description = "Email of existing user in PagerDuty who will receive alerts"
  type        = string
  sensitive   = true
}