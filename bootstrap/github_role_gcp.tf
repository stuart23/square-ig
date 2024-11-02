# Mostly taken from here: https://www.hashicorp.com/blog/access-google-cloud-from-hcp-terraform-with-workload-identity

resource "google_project" "plantsociety" {
  name       = "Plant Society"
  project_id = "plantsociety"
  org_id     = "1031939551432"
}


locals {
  services = toset([
    # MUST-HAVE for GitHub Actions setup
    "iam.googleapis.com",                  # Identity and Access Management (IAM) API
    "iamcredentials.googleapis.com",       # IAM Service Account Credentials API
    "cloudresourcemanager.googleapis.com", # Cloud Resource Manager API
    "sts.googleapis.com",                  # Security Token Service API
  ])
  roles = [
    "roles/iam.serviceAccountUser", # GitHub Actions identity
    "roles/editor",                 # allow to manage all resources

  ]
}

resource "google_project_service" "service" {
  for_each = local.services
  project  = google_project.plantsociety.project_id
  service  = each.value
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
  attribute_condition                = "attribute.repository == \"${var.github_org_name}/${var.github_repo_name}\""
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


# example service account that HCP Terraform will impersonate
resource "google_service_account_iam_member" "github_actions" {
  service_account_id = google_service_account.cicd_service_account.name
  role               = "roles/iam.workloadIdentityUser"
  member             = "principalSet://iam.googleapis.com/${google_iam_workload_identity_pool.pool.name}/attribute.repository/${var.github_org_name}/${var.github_repo_name}"
}


# Allow to access all resources
resource "google_project_iam_member" "roles" {
  project = google_project.plantsociety.project_id
  for_each = {
    for role in local.roles : role => role
  }
  role   = each.value
  member = "serviceAccount:${google_service_account.cicd_service_account.email}"
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