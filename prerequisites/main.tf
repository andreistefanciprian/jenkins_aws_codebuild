# define variables
variable "aws_access_key" {}
variable "aws_secret_key" {}

variable "region" {
  default = "us-east-1"
}

variable "aws_s3_bucket" {
  default = "s3-tfstate"
}
variable "aws_dynamodb_table" {
  default = "dynamodb-tfstate-lock"
}

# configure cloud provider
provider "aws" {
  access_key = var.aws_access_key
  secret_key = var.aws_secret_key
  region     = var.region
}

# generate unique names for dynamo db table and s3 bucket that will be used by terraform backend and remote state
resource "random_integer" "rand" {
  min = 10000
  max = 99999
}

locals {
  dynamodb_tfstate_lock_table_name = "${var.aws_dynamodb_table}-${random_integer.rand.result}"
  s3_tfstate_bucket_name  = "${var.aws_s3_bucket}-${random_integer.rand.result}"
}

# create dynamodb terraform lockstate table
resource "aws_dynamodb_table" "tf_statelock" {
  name           = local.dynamodb_tfstate_lock_table_name
  hash_key       = "LockID"
  read_capacity  = 20
  write_capacity = 20

  attribute {
    name = "LockID"
    type = "S"
  }
}

# create s3 bucket to be used by terraform as backend/remote state
resource "aws_s3_bucket" "tfstate" {
  bucket        = local.s3_tfstate_bucket_name
  acl           = "private"
  force_destroy = true

  versioning {
    enabled = true
  }

}

# output the names of built resources
output "s3_bucket" {
  value = aws_s3_bucket.tfstate.bucket
}

output "dynamodb_table" {
  value = aws_dynamodb_table.tf_statelock.name
}