variable "github_org_name" {
  type        = string
  default     = "stuart23"
  description = "The GitHub user or organization that contains the repo that will run actions as this role."
}

variable "github_repo_name" {
  type        = string
  default     = "square-ig"
  description = "The GitHub repo that will run actions as this role."
}