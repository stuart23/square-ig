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
credentials, execute the following from the `bootstrap` directory:

```
tf init && tf apply --var github_org_name=my_org_name --var github_repo_name=my_repo_name
```

This command will produce an output called `cicd_role_arn`. Take this ARN and
[create a GitHub Actions variable](https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/store-information-in-variables#creating-configuration-variables-for-a-repository)
called `CICD_ROLE_ARN` with the ARN as the value. Now create another variable called `AWS_REGION` with the
preferred AWS region (e.g. `us-east-1`) as the value.

This is a one-time setup, so there is no need to store the tf state file after it is created.


### Deployment


### Step 3 - Create and upload Square Credentials

An application needs to be created in Square and the credentials for the API need to be added to AWS Secrets Manager.

- Go to https://developer.squareup.com/apps/ and add a new application.
- Open AWS Secrets Manager
- Copy the Square Application ID to a new Plaintext AWS Secret called `square_application_id`
- Copy the Square Access token to a new Plaintext AWS Secret called `square_access_token`

After following the Instagram documentation on how to 


Square API version 2024-08-21