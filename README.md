## Description

This is a Jenkins pipeline that builds CodeBuild projects in AWS cloud, then runs these CodeBuild projects.
The CodeBuild projects are building infrastructure within AWS cloud.

The pipeline is doing the following:
- builds AWS Codebuild projects with terraform
- parse yaml file with codebuild projects to be run
- start each of the codebuild projects

## Prerequisites

Have Docker installed. We'll be running Jenkins on a Docker container.

Spin off a Jenkins docker container with a named volume to preserve jenkins configuration and pipeline for future use:
```docker run -p 8090:8080 -d -v jenkins_aws:/var/jenkins_home --name jenkins_aws jenkins/jenkins:2.235.1-lts-centos7```

Go through Jenkins installation by following steps at: http://localhost:8090.

Once Jenkins is configured, install these tools inside the Jenkins container:
```
# install tools in Jenkins container
docker container exec -ti -u root jenkins_aws bash
yum install -y python3 make
pip3 install -r requirements.txt

# install terraform
docker container exec -ti -u root jenkins_aws bash
curl -sk https://releases.hashicorp.com/terraform/0.12.26/terraform_0.12.26_linux_386.zip -o /tmp/terraform_0.12.26_linux_386.zip
unzip /tmp/terraform_0.12.26_linux_386.zip -d /usr/local/bin/
```

Define these secrets in Jenkins (http://localhost:8090):
 - AWS keys as secret text
 - Git token defined both as secret text and username and password type of secrets
 - AWS region defined as secret

Create Jenkins pipeline job with default settings using Pipeline script from SCM with URL https://github.com/andreistefanciprian/jenkins_aws_codebuild.git and configured git credentials.

## AWS cloud resources prerequsites

Because the pipeline uses terraform, we need an AWS s3 bucket (terraform backend) and dynamodb table for terraform state lock management.
Create these resources following these steps:
```
cd prerequisites
terraform init --var-file="../../terraform.tfvars"
terraform plan --var-file="../../terraform.tfvars" -out terraform.tfplan
terraform apply "terraform.tfplan"
```

For the steps above, AWS access key and access secret key should be stored in a terraform.tfvars file.
There is a sample with the contents of this file in the main directory of the repository.

Once the s3 bucket and dynamodb table are built, the names of these resources will be shown in the terraform output.
Take these names and populate the related fields in the backend section of the terraform code inside the main.tf files in codebuild, static and infra directories.

## Run pipeline

Access Jenkins at http://localhost:8090 and run pipeline job.

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
python3 execute_codebuild_from_yaml.py
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