# Bootstrap

This stack bootstraps the account to connect a role that can be used for Github Actions. This must be run manually before the repo can be connected to AWS.

To install the role, create AWS credentials for the account you want to use. In a terminal in this directory, then run `tf init && tf apply -var="github_org_name=<GITHUB ORG NAME> -var="github_repo_name=<GITHUB REPO NAME>`.

This stack just creates the OIDC connected role, so the tfstate isn't important to track.