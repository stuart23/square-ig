# Square-IG

This repo contains tooling for integrating the Square API with Instagram. The integration supports the following:

- Adding users in instagram when the user is added or updated in square.

## Setup

### Step 1 - Deploy CI/CD role.

The tooling is deployed into an AWS account using GitHub Actions. The first step is to setup an OIDC role in AWS
that Github Actions can use to deploy. To do this:

- Open the AWS console and navigate to CloudFormation.
- Go to 'Create Stack' > 'With new resources'.
- Select 'Choose an existing template' > 'Upload a template file'.
- Choose `GithubCICD.yml` from the cloudformation directory here.
- Click Next
- On the next screen, enter any name and then the github organization and repo details of your fork of this repo.
- Click through the prompts to deploy the stack. You will have to manually enable 'I acknowledge that AWS CloudFormation might create IAM resources with customised names.'
- Once the stack is deployed, navigate to in in the CloudFormation console and go to the outputs tab. You will need the `RoleARN` output value for the next step.

### Step 2 - 