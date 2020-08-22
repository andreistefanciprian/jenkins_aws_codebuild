## Description

This is a Jenkins pipeline that builds CodeBuild projects in AWS cloud, then runs these CodeBuild projects.
The CodeBuild projects are building infrastructure within AWS cloud.

The pipeline is doing the following:
- build AWS resources with terraform (Codebuild projects)
- parses yaml file with codebuild projects to be executed (python script)
- starts each of the codebuild projects extracted from yaml file, one by one (python script)

## Prerequisites

Have Docker installed. We'll be running Jenkins on a Docker container.

Spin off a Jenkins docker container with a named volume to preserve jenkins configuration and pipeline for future use:
```docker-compose -f jenkins/docker-compose.yaml up --detach```

AWS account at https://console.aws.amazon.com/.
AWS access key and secret to be used by Terraform and Jenkins.
AWS Role to be assumed by Terraform and Jenkins.
AWS s3 bucket (terraform backend) and dynamodb table for terraform state lock management.

Create these resources following these steps:
```
cd prerequisites
terraform init --var-file="../../terraform.tfvars"
terraform plan --var-file="../../terraform.tfvars" -out terraform.tfplan
terraform apply "terraform.tfplan"

# or

cd prerequisites
terraform init --var-file="../../terraform.tfvars"
terraform apply -input=false -auto-approve --var-file="../../terraform.tfvars"
```

For the steps above, AWS access key and access secret key should be stored in a terraform.tfvars file.
There is a sample with the contents of this file in the main directory of the repository.

Once the prerequsites resources are built, the details of these resources will be shown in the terraform output.
Take these details and populate the related fields in these files:
- terraform_code/*/main.tf (tfstate s3 bucket and dynamodb table)
- terraform_code/*/variables.tf (iam role arn)
- terraform_code/.env (AWS acess key and secret)
- buildspec.yaml (s3 bucket name)

## Configure Jenkins and run pipeline

Go through Jenkins installation steps at: http://localhost:8090. 

Define these secrets in Jenkins:
 - aws_access_key: AWS_ACCESS_KEY_ID (secret text); created in prerequsites step
 - aws_secret_key: AWS_SECRET_ACCESS_KEY (secret text); created in prerequsites step
 - aws_region: AWS region (secret text)
 - aws_account: AWS account number (secret text)
 - Git token defined both as secret text and username and password type of secrets (used for git hook and git clone private repo)

AWS credentials inside Codebuild projects:
- .env file with AWS secrets (AWS_ACCESS_KEY_ID=acces-key and AWS_SECRET_ACCESS_KEY=secret-key generated in prerequsites step) should be made available in s3 bucket (check buildspec.yaml file)
- terraform used by the CodeBuild projects is running inside a container (check docker-compose.yaml file)
- the terraform credentials are provided as environment variables via the .env file (check docker-compose.yaml file)

Create Jenkins pipeline job with default settings using Pipeline script from SCM with URL https://github.com/andreistefanciprian/jenkins_aws_codebuild.git.

Run pipeline job!

## Destroy resources at the end of this tutorial
```

# destroy terraform s3 bucket and dynamodb table used for tfstate management
cd prerequisites
terraform destroy --var-file="../../terraform.tfvars"

# destroy AWS resources (AWS creds to be stored in .env file prior to run these commands)
cd terraform_code
make destroy-auto-approve TF_TARGET=infra
make destroy-auto-approve TF_TARGET=static
make destroy-auto-approve TF_TARGET=codebuil

# spin down Jenkins docker container:
docker-compose -f jenkins/docker-compose.yaml down
```

## Other debug commands

Use these AWS CLI commands to manually interact with CodeBuild:
```
# list CodeBuild projects and builds
aws codebuild list-projects
aws codebuild list-builds

# start CodeBuild project
aws codebuild start-build --project-name codebuildtest-MessageUtil
aws codebuild start-build --project-name newproj-test

# list CodeBuild jobs for specific project
aws codebuild list-builds-for-project --project-name codebuildtest-MessageUtil

# get last build for project
aws codebuild list-builds-for-project --project-name codebuildtest-MessageUtil --query 'ids[0]' --output text

aws codebuild batch-get-builds --ids codebuildtest-MessageUtil:f0682dfe-2d7e-4bec-8061-2008843089e7

# query status of last Codebuild build
build_id=$(aws codebuild list-builds-for-project --project-name codebuildtest-MessageUtil --query 'ids[0]' --output text)
aws codebuild batch-get-builds --ids $build_id --query 'builds[0].buildStatus' --output text
```

Use these commands to manually check python script:
```
# create python3 virtual env
python3 -m venv .venv

# activate environment
source .venv/bin/activate

# install requirements
pip install -r requirements.txt

# execute script
aws_account=9238748923565 
python execute_codebuild_from_yaml.py $aws_account
```

Use these commands to verify you can build resources with terraform from CLI:
```
TF_VAR_TARGET=static
docker-compose run terraform init $TF_VAR_TARGET
docker-compose run terraform plan -out terraform.tfplan $TF_VAR_TARGET
docker-compose run terraform apply terraform.tfplan
docker-compose run terraform destroy -auto-approve $TF_VAR_TARGET

# using make commands
make deploy-auto-approve TF_TARGET=$TF_VAR_TARGET
make destroy-auto-approve TF_TARGET=$TF_VAR_TARGET
```