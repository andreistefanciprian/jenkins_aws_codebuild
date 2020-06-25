
# Output variable definitions

output "iam_role_name" {
  value       = aws_iam_role.codebuild_static.name
  description = "The name of the IAM Role."
}
output "iam_role_arn" {
  value       = aws_iam_role.codebuild_static.arn
  description = "The Amazon Resource Name (ARN) specifying the IAM Role."
}

output "aws_iam_role_policy_name" {
  value       = aws_iam_role_policy.codebuild_static_policy.name
  description = "The name of the IAM Role Policy."
}

output "codebuild_project_id" {
  value       = aws_codebuild_project.example.id
  description = "The name (if imported via name) or ARN (if created via Terraform or imported via ARN) of the CodeBuild project."
}

output "codebuild_project_arn" {
  value       = aws_codebuild_project.example.arn
  description = "The ARN of the CodeBuild project."
}