# Square-IG

This repo contains tooling for integrating the Square API with Instagram. The integration supports the following:

- Adding users in instagram when the user is added or updated in square.
- Creating QR codes when an item is updated in square.

## Setup

This repo uses GitHub Actions to deploy infrastructure to AWS. To setup this workflow, GitHub Actions first needs
to be able to authenticate to AWS. Infrastructure is then managed by Terraform using the AWS account as the state
store.

### Bootstrap

Before deploying any application, the AWS account must first be bootstrapped so that it has the role to allow
GitHub Actions to deploy resources, and a store for the Terraform state. To bootstrap, in a shell with AWS 
and GCP auth (`gcloud auth application-default login`), execute the following from the `bootstrap` directory:

```
tf init && tf apply --var github_org_name=my_org_name --var github_repo_name=my_repo_name
```

This command will produce an output called `cicd_role_arn` and `cicd_service_account`. Take `cicd_role_arn` and
[create a GitHub Actions variable](https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/store-information-in-variables#creating-configuration-variables-for-a-repository)
called `CICD_ROLE_ARN` with the ARN as the value. Create variables with the following keys and values:

- `AWS_REGION` = the preferred AWS region (e.g. `us-east-1`).
- `gcp_workload_identity_provider` = Output value of `service_account` - CICD Service Account
- `cicd_service_account` = Output value of `workload_identity_provider` - Workload Identity Provider
- `gcp_project` = Output value of `gcp_project` - Workload Identity Provider

This is a one-time setup, so there is no need to store the tf state file after it is created.

### Setup google drive
Create a google drive and share it with the email address given in the `service_account` output from terraform.
You should give it Content Manager (or Manager?) permissions to read and write to the drive.
Setup another Github Actions `drive_name` = Name of the google drive to use.

If you get a 404 error in the `Get Google Drive ID` Github actions step, the drive may not have been shared
correctly.

### Deployment


### Step 3 - Create and upload Square Credentials

An application needs to be created in Square and the credentials for the API need to be added to AWS Secrets Manager.

- Go to https://developer.squareup.com/apps/ and add a new application.
- Open AWS Secrets Manager
- Copy the Square Application ID to a new Plaintext AWS Secret called `square_application_id`
- Copy the Square Access token to a new Plaintext AWS Secret called `square_access_token`

After following the Instagram documentation on how to 


Square API version 2024-08-21

### Alerting

Alerting is done via PagerDuty. You can sign up for a free account to use it with this application.

Once signed up, create an API key by following [these instructions](https://support.pagerduty.com/main/docs/api-access-keys#generate-a-general-access-rest-api-key)
Copy the API key to a new GitHub Actions secret called `PAGERDUTY_API_KEY`.

Also create another secret called `PAGERDUTY_EMAIL` with the email of account that should receive the alerts.