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
- On the next screen, enter any name and then the github user or organization and repo name of your fork of this repo. For example, if the repo URL is https://github.com/stuart23/square-ig/, the user or organization is 'stuart23', and the repo name is 'square-ig'. 
- Click through the prompts to deploy the stack. You will have to manually enable 'I acknowledge that AWS CloudFormation might create IAM resources with customised names.'
- Once the stack is deployed, navigate to in in the CloudFormation console and go to the outputs tab. You will need the `RoleARN` and `StackRegion` output value for the next step.

### Step 2 - Add AWS Role to Github

Now that there is a Role in AWS that can deploy the rest of the tooling, we need to tell Github the roles details so it can use it.

- In your Github repo, go to Settings > Secrets and variables > Actions
- Click 'New Repository Secret'
- Enter 'cloudformation_role_arn' for the secret name. This cannot change as it is referenced in the Github Action with this name.
- In the secret value, enter the output RoleARN from the CloudFormation stack output in step 1.
- Create a second secret following the same process. In this secret, the name shouls be 'aws_region', and the value is the StackRegion from the CloudFormation stack output.

### Step 3 - Create Instagram User Access Token Secret

After following the Instagram documentation on how to 


Square API version 2024-08-21