pipeline {

   agent any

   environment {
      AWS_ACCESS_KEY_ID = credentials('aws_access_key')
      AWS_REGION = credentials('aws_region')
      AWS_DEFAULT_REGION = credentials('aws_region')
      AWS_SECRET_ACCESS_KEY = credentials('aws_secret_key')
      TF_IN_AUTOMATION = "true"
      AWS_ACCOUNT = credentials('aws_account')
   }

   stages {

      // stage('CLEAN WORKING DIR & GIT CHECKOUT') {
      //    steps {
      //          cleanWs()  
      //          checkout scm
      //    }
      // }

      // stage('Build CodeBuild projects with Terraform') {
      //    steps {
      //          echo 'Building AWS CodeBuild Projects...'
      //          dir('terraform_code/'){
      //             sh "make deploy-auto-approve TF_TARGET=codebuild TF_EXEC=terraform"
      //          }                
      //    }
      // }

      stage('Execute CodeBuild projects in AWS') {
         steps {
            sh '''
            aws sts get-caller-identity
            aws sts assume-role --role-arn "arn:aws:iam::${AWS_ACCOUNT}:role/test-role" --role-session-name jenkins --duration-seconds 3600 --external-id smth
            '''

            echo 'Parse yaml and execute CodeBuild Projects...'
            sh 'python3 -u execute_codebuild_from_yaml.py $AWS_ACCOUNT'
         }
      }

      // stage('Destroy CodeBuild projects with Terraform') {
      //    steps {
      //          echo 'Destroying AWS CodeBuild Projects...'
      //          dir('terraform_code/'){
      //             sh "make destroy-auto-approve TF_TARGET=codebuild TF_EXEC=terraform"
      //          }                
      //    }
      // }

   }
}
