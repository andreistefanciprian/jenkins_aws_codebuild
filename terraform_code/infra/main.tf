

# aws cloud provider
provider "aws" {
  region = var.region

  # assume_role {
  #   role_arn    = var.cloud_assume_role ? var.arn_role : null
  #   external_id = var.cloud_assume_role ? var.extenal_id : null
  #   session_name = var.cloud_assume_role ? var.session_name : null
  #   duration_seconds = var.cloud_assume_role ? var.session_duration : null
  # }

}

# terraform backend
terraform {
  backend "s3" {
    bucket         = "s3-tfstate-83086"
    key            = "infra/infra.tfstate"
    region         = "us-east-1"
    dynamodb_table = "dynamodb-tfstate-lock-83086"
  }
}

# terraform remote state
data "terraform_remote_state" "static" {
  backend = "s3"

  config = {
    key    = "static/static.tfstate"
    bucket = var.static_remote_state_bucket
    region = var.region
  }
}

# aws EC2 instance
resource "aws_instance" "foo" {
  ami           = "ami-039a49e70ea773ffc" # us-west-2
  instance_type = "t2.micro"

  subnet_id = element(data.terraform_remote_state.static.outputs.public_subnets, 0)
}