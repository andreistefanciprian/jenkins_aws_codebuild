## Description

Jenkins pipeline that triggers CodeBuild jobs in AWS.

## Prerequisites

Have Docker installed. We'll be running Jenkins on a Docker container.
Spin off a jenkins docker container with a named volume to preserve jenkins configuration and pipeline for future use:

```docker run -p 8090:8080 -d -v jenkins_aws:/var/jenkins_home --name jenkins_aws jenkins/jenkins:2.235.1-lts-centos7```

Have AWS account with CodeBuild jobs configured. The names of the CodeBuild projects should be made available in the yaml file.
Have aws cli installed on jenkins machine (https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2-linux.html).
Have python3 and pip packages installed in Jenkins:
```
yum install -y python3
pip3 install -r requirements.txt
```

AWS keys defined in Jenkins as secret text.
Git token defined both as secret text and username and password type of secrets.
Aws region defined as secret.

## AWS resources prerequsites

Have aws s3 bucket for terraform backend and dynamodb table for terraform state lock management:
```
cd prerequisites
terraform init --var-file="../../terraform.tfvars"
terraform plan --var-file="../../terraform.tfvars" -out terraform.tfplan
terraform apply "terraform.tfplan"

# destroy resources at the end of this tutorial
terraform destroy --var-file="../../terraform.tfvars"
```

For the step above, AWS access key and access secret key should be stored in a terraform.tfvars.
There is a sample with the contents of this file in the main directory of the repository.

Once s3 bucket and dynamodb table are built, the names of these resources will be shown in the terraform output.
Take these names and populate the related fields in the backend section of the terraform code inside the main.tf files in both static and infra directories.

## DEBUG: Use these AWS CLI commands to manually interact with CodeBuild

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

## DEBUG: Use these commands to manually check python script
```
# create python3 virtual env
python3 -m venv .venv

# activate environment
source .venv/bin/activate

# install requirements
pip install -r requirements.txt

# execute script
python3 ...
```

## DEBUG: Use these commands to verify you can build resources with terraform from CLI

AWS creds to be stored in .env file prior to run these commands.

```
docker-compose run terraform init
docker-compose run terraform plan -out terraform.tfplan
docker-compose run terraform apply "terraform.tfplan"
docker-compose run terraform destroy --auto-approve
```