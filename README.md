# Square-IG

This repo contains tooling for integrating the Square API with Instagram. The integration supports the following:

- Adding users in instagram when the user is added or updated in square.

## Setup

### Terraform Cloud

Deployment is done through Terraform Cloud. The easiest way I have found to bootstrap Terraform cloud with Github and AWS is:

1. If you haven't already done so, sign up for a Terraform Cloud account and create an organization.
2. Clone the Hashicorp repo for setting up OIDC roles:
   ```
   git clone git@github.com:hashicorp/terraform-dynamic-credentials-setup-examples.git
   ```
3. Configure the AWS CLI credentials `AWS_ACCESS_KEY_ID` & `AWS_SECRET_ACCESS_KEY` in the terminal.
4. Get a Terraform user token from [here](https://app.terraform.io/app/settings/tokens), it will just be used to create these resources, so you can have a 1 hour expiry. Set the env var `TFE_TOKEN` to this token.
5. Run the following to deploy the AWS role. A new Terraform workspace will be created, so you can give it whatever name you want
   ```
   tf init && tf apply --var tfc_organization_name=<<YOUR TERRAFORM ORG NAME>> --var tfc_workspace_name=<<A NAME FOR THE WORKSPACE>>
   ```
   e.g.
   ```
   tf init && tf apply --var tfc_organization_name=tiny_plant_store --var tfc_workspace_name=ig-square
   ```

After creating the Terraform Cloud Workspace you can then install the Github application into the Terraform Cloud workspace.


### Step 3 - Create and upload Square Credentials

An application needs to be created in Square and the credentials for the API need to be added to AWS Secrets Manager.

- Go to https://developer.squareup.com/apps/ and add a new application.
- Open AWS Secrets Manager
- Copy the Square Application ID to a new Plaintext AWS Secret called `square_application_id`
- Copy the Square Access token to a new Plaintext AWS Secret called `square_access_token`

After following the Instagram documentation on how to 


Square API version 2024-08-21