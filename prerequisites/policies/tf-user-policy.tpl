{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AllowBackend",
            "Effect": "Allow",
            "Action": [
                "s3:*",
                "iam:ListRoles",
                "dynamodb:*"
            ],
            "Resource": "*"
        },
        {
            "Sid": "TerraformAssumeRole",
            "Effect": "Allow",
            "Action": "sts:AssumeRole",
            "Resource": "arn:aws:iam::${aws_account}:role/${role_name}"
        }
    ]
}