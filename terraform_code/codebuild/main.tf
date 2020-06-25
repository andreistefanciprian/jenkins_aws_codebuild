# terraform cloud provider
provider "aws" {
  region = var.region
}

# terraform backend
terraform {
  backend "s3" {
    bucket         = "s3-tfstate-95653"
    key            = "static/static.tfstate"
    region         = "us-east-1"
    dynamodb_table = "dynamodb-tfstate-lock-95653"
  }
}


resource "aws_iam_role" "codebuild_static" {
  name = "codebuild_static"

  assume_role_policy = file("codebuild/policies/user_role.json")
}

resource "aws_iam_role_policy" "codebuild_static_policy" {
  name = "codebuild_static_policy"
  role = aws_iam_role.codebuild_static.id

  policy = file("codebuild/policies/user_role_policy.json")
}


resource "aws_codebuild_project" "example" {
  name          = "test-project"
  description   = "test_codebuild_project"
  build_timeout = "5"
  service_role  = aws_iam_role.codebuild_static.arn

  artifacts {
    type = "NO_ARTIFACTS"
  }

  environment {
    compute_type                = "BUILD_GENERAL1_SMALL"
    image                       = "aws/codebuild/amazonlinux2-x86_64-standard:3.0"
    type                        = "LINUX_CONTAINER"
    image_pull_credentials_type = "CODEBUILD"

    environment_variable {
      name  = "TF_ACTION"
      value = "deploy"
      type  = "PLAINTEXT"
    }

    environment_variable {
      name  = "TF_VAR_TARGET"
      value = "static"
      type  = "PLAINTEXT"
    }

    privileged_mode = true

  }

  source {
    type            = "GITHUB"
    location        = "https://github.com/andreistefanciprian/jenkins_aws_codebuild.git"
    git_clone_depth = 1

    git_submodules_config {
      fetch_submodules = true
    }
  }

  source_version = "master"

  tags = {
    Environment = "Test"
  }
}
