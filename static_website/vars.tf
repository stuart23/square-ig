variable "domain_name" {
  type        = string
  description = "Name of the domain"
}

variable "stack_name" {
  type        = string
  default     = "static_website"
  description = "Name of the stack"
}