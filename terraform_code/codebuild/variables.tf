variable "region" {
  default = "us-east-1"
}

variable "name" {
  description = "AWS resource name."
  type = string
  default = "deploy_static"
}

variable "description" {
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