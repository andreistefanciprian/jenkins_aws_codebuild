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