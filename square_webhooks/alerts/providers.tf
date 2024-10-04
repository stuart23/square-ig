terraform {
  required_version = "~> 1.9.5"
  required_providers {
    pagerduty = {
      source  = "pagerduty/pagerduty"
      version = ">= 2.2.1"
    }
  }
}


provider "pagerduty" {
  token = var.pagerduty_api_key
}