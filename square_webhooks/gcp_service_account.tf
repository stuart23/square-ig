# Mostly taken from here: https://www.hashicorp.com/blog/access-google-cloud-from-hcp-terraform-with-workload-identity

data "google_project" "project" {}


data "aws_caller_identity" "current" {}


resource "google_iam_workload_identity_pool" "pool" {
  project                   = data.google_project.project.project_id
  workload_identity_pool_id = "aws-pool"
}


resource "google_iam_workload_identity_pool_provider" "aws" {
  project                            = data.google_project.project.project_id
  workload_identity_pool_id          = google_iam_workload_identity_pool.pool.workload_identity_pool_id
  workload_identity_pool_provider_id = "aws-pool"
  display_name                       = "AWS WI Pool"
  description                        = "AWS identity pool provider for accessing Service Accounts"
  # attribute_condition                = "assertion.arn.startsWith('arn:aws:sts::AWS_ACCOUNT_ID:role/')"
  attribute_condition                = "assertion.arn==\"${aws_iam_role.lambda_role.arn}\""
  attribute_mapping = {
    "google.subject"       = "assertion.arn"
    "attribute.account"= "assertion.account"
    "attribute.aws_role"="assertion.arn.extract('role/{role}/')"
    # "attribute.aws_ec2_instance"="assertion.arn.extract('assumed-role/{role_and_session}').extract('/{session}')"
  }
  aws {
    account_id = data.aws_caller_identity.current.account_id
  }
}


resource "google_service_account" "lambda_service_account" {
  project      = data.google_project.project.project_id
  account_id   = "lambda-role"
  display_name = "Service account used by AWS Lambda Function"
}


resource "google_service_account_iam_member" "lambda_service_account_member" {
  service_account_id = google_service_account.lambda_service_account.name
  role               = "roles/iam.workloadIdentityUser"
  member             = "principalSet://iam.googleapis.com/${google_iam_workload_identity_pool.pool.name}/attribute.aws_role/${aws_iam_role.lambda_role.arn}"
}


# Allow to access all resources
resource "google_project_iam_member" "roles" {
  project = data.google_project.project.project_id
  role   = "roles/iam.serviceAccountUser"
  member = "serviceAccount:${google_service_account.lambda_service_account.email}"
}


resource "google_project_iam_member" "roles" {
  project = data.google_project.project.project_id
  role   = "roles/viewer"
  member = "serviceAccount:${google_service_account.lambda_service_account.email}"
}


output "workload_identity_provider" {
  description = "Lambda workload identity pool"
  value       = google_iam_workload_identity_pool_provider.aws.name
}


output "service_account" {
  description = "Labels service account"
  value       = google_service_account.lambda_service_account.email
}