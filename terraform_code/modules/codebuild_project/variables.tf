

variable "codebuild_project_name" {
  description = "AWS resource name."
  type = string
  default = "deploy_static"
}

variable "codebuild_project_description" {
  description = "Description of AWS resource."
  type = string
  default = "CodeBuild project."
}

variable "tf_action" {
  description = "Terraform action to execute: deploy/destroy."
  type = string
  default = "deploy"
}

variable "tf_target" {
  description = "terraform resources to build. Eg: static/infra."
  type = string
  default = "static"
}

variable "git_repo_link" {
  description = "Github repository link."
  type = string
  default = "https://github.com/andreistefanciprian/jenkins_aws_codebuild.git"
}

variable "git_repo_branch" {
  description = "Github repository branch."
  type = string
  default = "master"
}

variable "iam_role_name" {
  description = "AWS resource name."
  type = string
  default = "codebuild_iam_role_deploy_static"
}

variable "iam_role_policy_name" {
  description = "AWS resource name."
  type = string
  default = "codebuild_iam_role_policy_deploy_static"
}

variable "codebuild_tags" {
  description = "Tags to set on the codebuild project."
  type = map(string)
  default = {
    Terraform   = "true"
    Environment = "dev"
  }
}