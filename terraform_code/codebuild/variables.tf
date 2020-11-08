variable "region" {
  default = "us-east-1"
}

variable "cloud_assume_role" {
  type    = bool
  default = true
}

variable "arn_role" {
  type    = string
  default = "arn:aws:iam::396667666940:role/tf_role"
}

variable "extenal_id" {
  type    = string
  default = "smth"
}

variable "session_name" {
  type    = string
  default = "Jenkins"
}

variable "session_duration" {
  type    = number
  default = 3600
}

variable "git_repo_branch" {
  type    = string
  default = "feature/display-codebuild-logs"
}

