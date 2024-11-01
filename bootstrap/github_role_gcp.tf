resource "google_project" "plantsociety" {
  name       = "Plant Society"
  project_id = "plantsociety"
  org_id     = "1031939551432"
}


resource "google_project_service" "cloudapis" {
  project = google_project.plantsociety.project_id
  service = "cloudapis.googleapis.com"
}


resource "google_iam_workload_identity_pool" "pool" {
  project                   = google_project.plantsociety.project_id
  workload_identity_pool_id = "square-integrations-pool"
}


resource "google_iam_workload_identity_pool_provider" "github_actions" {
  project                            = google_project.plantsociety.project_id
  workload_identity_pool_id          = google_iam_workload_identity_pool.pool.workload_identity_pool_id
  workload_identity_pool_provider_id = "githubactions"
  display_name                       = "GitHub Actions"
  description                        = "GitHub Actions identity pool provider for automated test"
  attribute_condition = <<EOT
    attribute.repository == "${var.github_org_name}/${var.github_repo_name}"
EOT
  attribute_mapping = {
    "google.subject"       = "assertion.sub"
    "attribute.actor"      = "assertion.actor"
    "attribute.aud"        = "assertion.aud"
    "attribute.repository" = "assertion.repository"
  }
  oidc {
    issuer_uri = "https://token.actions.githubusercontent.com"
  }
}


resource "google_service_account" "cicd_service_account" {
  project      = google_project.plantsociety.project_id
  account_id   = "cicd-role"
  display_name = "Service account used by Github Actions"
}


resource "google_service_account_iam_binding" "admin_account_iam" {
  service_account_id = google_service_account.cicd_service_account.name
  role               = "roles/editor"

  members = [
    "principalSet://iam.googleapis.com/${google_iam_workload_identity_pool.pool.name}/attribute.repository/${var.github_org_name}/${var.github_repo_name}",
  ]
}


output "workload_identity_provider" {
  description = "GitHub actions workload identity pool"
  value       = google_iam_workload_identity_pool_provider.github_actions.name
}


output "gcp_project" {
  description = "GitHub actions project"
  value       = google_project.plantsociety.project_id
}


output "service_account" {
  description = "GitHub actions project"
  value       = google_service_account.cicd_service_account.email
}