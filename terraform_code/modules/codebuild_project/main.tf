


resource "aws_iam_role" "default" {
  name = var.iam_role_name

  assume_role_policy = file("modules/codebuild_project/policies/user_role.json")
}

resource "aws_iam_role_policy" "default" {
  name = var.iam_role_policy_name
  role = aws_iam_role.default.id

  policy = file("modules/codebuild_project/policies/user_role_policy.json")
}


resource "aws_codebuild_project" "example" {
  name          = var.codebuild_project_name
  description   = var.codebuild_project_description
  build_timeout = "5"
  service_role  = aws_iam_role.default.arn

  artifacts {
    type = "NO_ARTIFACTS"
  }

  environment {
    compute_type                = "BUILD_GENERAL1_SMALL"
    image                       = "aws/codebuild/amazonlinux2-x86_64-standard:3.0"
    type                        = "LINUX_CONTAINER"
    image_pull_credentials_type = "CODEBUILD"

    environment_variable {
      name  = "TF_ACTION"
      value = var.tf_action
      type  = "PLAINTEXT"
    }

    environment_variable {
      name  = "TF_VAR_TARGET"
      value = var.tf_target
      type  = "PLAINTEXT"
    }

    privileged_mode = true

  }

  source {
    type            = "GITHUB"
    location        = var.git_repo_link
    git_clone_depth = 1

    git_submodules_config {
      fetch_submodules = true
    }
  }

  source_version = var.git_repo_branch

  tags = var.codebuild_tags

  logs_config {
    cloudwatch_logs {
      group_name = "cw-cb-group"
      stream_name = var.tf_target
    }
  }
}
