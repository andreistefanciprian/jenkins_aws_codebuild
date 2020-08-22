# terraform cloud provider
provider "aws" {
  region = var.region

  assume_role {
    role_arn         = var.cloud_assume_role ? var.arn_role : null
    external_id      = var.cloud_assume_role ? var.extenal_id : null
    session_name     = var.cloud_assume_role ? var.session_name : null
    duration_seconds = var.cloud_assume_role ? var.session_duration : null
  }

}

# terraform backend
terraform {
  backend "s3" {
    bucket         = "s3-tfstate-60303"
    key            = "static/static.tfstate"
    region         = "us-east-1"
    dynamodb_table = "dynamodb-tfstate-lock-60303"
  }
}

# aws vpc
data "aws_availability_zones" "available" {}

module "vpc" {
  source = "terraform-aws-modules/vpc/aws"

  name = var.name
  cidr = var.cidr_block

  azs             = slice(data.aws_availability_zones.available.names, 0, var.subnet_count)
  private_subnets = var.private_subnets
  public_subnets  = var.public_subnets

  enable_nat_gateway = false
  enable_vpn_gateway = false

  tags = {
    Terraform   = "true"
    Environment = "dev"
  }
}


