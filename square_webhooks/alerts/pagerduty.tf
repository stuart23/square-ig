resource "pagerduty_user" "alerts_email" {
  name  = "Alert Receiver"
  email = var.pagerduty_email
}


resource "pagerduty_escalation_policy" "square_integration_alerts" {
  name        = "square_integration_alerts"
  description = "Square Integration Alerts"
  num_loops   = 2

  rule {
    escalation_delay_in_minutes = 10

    target {
      type = "user_reference"
      id   = pagerduty_user.alerts_email.id
    }
  }
}


resource "pagerduty_service" "square_integration_alerts" {
  name                    = "square_integration_alerts"
  auto_resolve_timeout    = 14400
  acknowledgement_timeout = 600
  escalation_policy       = pagerduty_escalation_policy.square_integration_alerts.id
  alert_creation          = "create_alerts_and_incidents"

  auto_pause_notifications_parameters {
    enabled = true
    timeout = 300
  }
}


data "pagerduty_vendor" "cloudwatch" {
  name = "Cloudwatch"
}


resource "pagerduty_service_integration" "square_integration_alerts_cloudwatch" {
  name    = "square_integration_alerts_cloudwatch"
  service = pagerduty_service.square_integration_alerts.id
  vendor  = data.pagerduty_vendor.cloudwatch.id
}