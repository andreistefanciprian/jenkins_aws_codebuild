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
  version    = "3.3.0"
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
  s3_tfstate_bucket_name           = "${var.aws_s3_bucket}-${random_integer.rand.result}"
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

# IAM policies
variable "role_name" {
  default = "tf_role"
}

variable "aws_account" {}

variable "aws_iam_user" {
  default = "tf_user"
}

variable "external_id" {
  default = "smth"
}


# IAM Role
resource "aws_iam_role" "default" {
  name               = var.role_name
  assume_role_policy = templatefile("policies/tf-role-trust-policy.tpl", { aws_account = var.aws_account, aws_iam_user = var.aws_iam_user, external_id = var.external_id })
}

resource "aws_iam_role_policy" "default" {
  name   = var.role_name
  role   = aws_iam_role.default.id
  policy = file("policies/tf-role-policy.json")
}

# IAM User
resource "aws_iam_user" "default" {
  name = var.aws_iam_user
}

resource "aws_iam_user_policy" "default" {
  name   = var.aws_iam_user
  user   = aws_iam_user.default.name
  policy = templatefile("policies/tf-user-policy.tpl", { aws_account = var.aws_account, role_name = var.role_name })
}

# IAM key
resource "aws_iam_access_key" "default" {
  user = aws_iam_user.default.name
}

# output the names of built resources
output "s3_bucket" {
  value = aws_s3_bucket.tfstate.bucket
}

output "dynamodb_table" {
  value = aws_dynamodb_table.tf_statelock.name
}

output "iam_role_arn" {
  value = aws_iam_role.default.arn
}

output "iam_user_arn" {
  value = aws_iam_user.default.arn
}

output "iam_access_key_id" {
  value = aws_iam_access_key.default.id
}

output "iam_secret" {
  value = aws_iam_access_key.default.secret
}