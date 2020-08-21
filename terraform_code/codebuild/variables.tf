variable "region" {
  default = "us-east-1"
}

variable "cloud_assume_role" {
  type = bool
  default = false
}

variable "arn_role" {
  type = string
  default = "arn:aws:iam::1234567890:role/test-role"
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
