# terraform cloud provider
provider "aws" {
  region = var.region
}

# terraform backend
terraform {
  backend "s3" {
    bucket         = "s3-tfstate-95653"
    key            = "codebuild/codebuild.tfstate"
    region         = "us-east-1"
    dynamodb_table = "dynamodb-tfstate-lock-95653"
  }
}


module "codebuild_deploy_static" {
  source = "../modules/codebuild_project"
  codebuild_project_name = "deploy_static"
  codebuild_project_description = "Deploy static layer resources"
  tf_action = "deploy"
  tf_target = "static"
  git_repo_link = "https://github.com/andreistefanciprian/jenkins_aws_codebuild.git"
  git_repo_branch = "master"
  iam_role_name = "iam_role_deploy_static"
  iam_role_policy_name = "iam_role_policy_deploy_static"

  codebuild_tags = {
    Env   = "test"
    Layer = "static"
  }
}

module "codebuild_deploy_infra" {
  source = "../modules/codebuild_project"
  codebuild_project_name = "deploy_infra"
  codebuild_project_description = "Deploy infra layer resources"
  tf_action = "deploy"
  tf_target = "infra"
  git_repo_link = "https://github.com/andreistefanciprian/jenkins_aws_codebuild.git"
  git_repo_branch = "master"
  iam_role_name = "iam_role_deploy_infra"
  iam_role_policy_name = "iam_role_policy_deploy_infra"

  codebuild_tags = {
    Env   = "test"
    Layer = "infra"
  }
}

module "codebuild_destroy_static" {
  source = "../modules/codebuild_project"
  codebuild_project_name = "destroy_static"
  codebuild_project_description = "Destroy static layer resources"
  tf_action = "destroy"
  tf_target = "static"
  git_repo_link = "https://github.com/andreistefanciprian/jenkins_aws_codebuild.git"
  git_repo_branch = "master"
  iam_role_name = "iam_role_destroy_static"
  iam_role_policy_name = "iam_role_policy_destroy_static"

  codebuild_tags = {
    Env   = "test"
    Layer = "static"
  }
}

module "codebuild_destroy_infra" {
  source = "../modules/codebuild_project"
  codebuild_project_name = "destroy_infra"
  codebuild_project_description = "Destroy infra layer resources"
  tf_action = "destroy"
  tf_target = "infra"
  git_repo_link = "https://github.com/andreistefanciprian/jenkins_aws_codebuild.git"
  git_repo_branch = "master"
  iam_role_name = "iam_role_destroy_infra"
  iam_role_policy_name = "iam_role_policy_destroy_infra"

  codebuild_tags = {
    Env   = "test"
    Layer = "infra"
  }
}