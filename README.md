## Description

Jenkins pipeline that triggers CodeBuild jobs in AWS.

## Prerequisites

Have Docker installed. We'll be running Jenkins on a Docker container.
Spin off a jenkins docker container with a named volume to preserve jenkins configuration and pipeline for future use:
```docker run -p 8080:8080 -d -v jenkins_home_centos:/var/jenkins_home --name jenkins jenkins/jenkins:lts-centos```

```docker run -p 8090:8080 -d -v jenkins_aws:/var/jenkins_home --name jenkins_aws jenkins/jenkins:2.235.1-lts-centos7```

Have AWS account.
Have aws cli installed on jenkins machine (https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2-linux.html).
Have Pipeline Utility Steps plugin installed to use 

## AWS CLI CodeBuild commands

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


```
# create python3 virtual env
python3 -m venv .venv

# activate environment
source .venv/bin/activate

# install requirements
pip install -r requirements.txt

# execute script
python3 

```