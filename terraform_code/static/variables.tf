variable "region" {
  default = "us-east-1"
}

variable "name" {
  default = "lab2"
}


variable "subnet_count" {
  default = 2
}

variable "cidr_block" {
  default = "10.0.0.0/16"
}

variable "private_subnets" {
  type    = list
  default = ["10.0.1.0/24", "10.0.3.0/24"]
}

variable "public_subnets" {
  type    = list
  default = ["10.0.31.0/24", "10.0.33.0/24"]
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

