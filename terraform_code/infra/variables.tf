# define variables
variable "region" {
  default = "us-east-1"
}

variable "static_remote_state_bucket" {
  default = "s3-tfstate-60303"
}

variable "cloud_assume_role" {
  type = bool
  default = true
}

variable "arn_role" {
  type = string
  default = "arn:aws:iam::396667666940:role/test-role"
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