

# aws cloud provider
provider "aws" {
  region     = var.region
}

# terraform backend
terraform {
  backend "s3" {
    bucket = "s3-tfstate-95653"
    key    = "infra/infra.tfstate"
    region = "us-east-1"
    dynamodb_table = "dynamodb-tfstate-lock-95653"
  }
}

# terraform remote state
data "terraform_remote_state" "static" {
  backend = "s3"

  config = {
    key     = "static/static.tfstate"
    bucket  = var.static_remote_state_bucket
    region  = var.region
  }
}

# aws EC2 instance
resource "aws_instance" "foo" {
  ami           = "ami-039a49e70ea773ffc" # us-west-2
  instance_type = "t2.micro"

  subnet_id = element(data.terraform_remote_state.static.outputs.public_subnets, 0)
}