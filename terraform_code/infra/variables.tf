# define variables
variable "region" {
  default = "us-east-1"
}

variable "static_remote_state_bucket" {
  default = "s3-tfstate-83086"
}

variable "cloud_assume_role" {
  type = bool
  default = false
}

variable "arn_role" {
  type = string
}

variable "extenal_id" {
  type = string
  default = "smth"
}

variable "session_name" {
  type = string
  default = "Jenkins"
}
variable "session_duration" {
  type = number
  default = 3600
}