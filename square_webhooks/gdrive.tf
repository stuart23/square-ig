data "google_project" "plantsociety_project" {}


resource "google_project_service" "cloudapis" {
  project = google_project.plantsociety_project.project_id
  service = "drive.googleapis.com"
}