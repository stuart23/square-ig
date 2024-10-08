variable "domain_name" {
  type        = string
  description = "Name of the domain"
}

variable "porkbun_api_key" {
  type      = string
  sensitive = true
}

variable "porkbun_secret_key" {
  type      = string
  sensitive = true
}

variable "aws_region" {
  type        = string
  description = "The region to deploy into"
}