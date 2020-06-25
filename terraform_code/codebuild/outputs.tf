output "codebuild_deploy_static_arn" {
  description = "Name of the CodeBuild project"
  value       = module.codebuild_deploy_static.codebuild_project_arn
}

output "codebuild_deploy_infra_arn" {
  description = "Name of the CodeBuild project"
  value       = module.codebuild_deploy_infra.codebuild_project_arn
}

output "codebuild_destroy_static_arn" {
  description = "Name of the CodeBuild project"
  value       = module.codebuild_destroy_static.codebuild_project_arn
}

output "codebuild_destroy_infra_arn" {
  description = "Name of the CodeBuild project"
  value       = module.codebuild_destroy_infra.codebuild_project_arn
}