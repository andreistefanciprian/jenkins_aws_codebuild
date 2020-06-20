pipeline {

   agent any

   environment {
      AWS_ACCESS_KEY_ID = credentials('aws_access_key')
      AWS_REGION = credentials('aws_region')
      AWS_DEFAULT_REGION = credentials('aws_region')
      AWS_SECRET_ACCESS_KEY = credentials('aws_secret_key')
   }

   stages {

      stage('CLEAN WORKING DIR & GIT CHECKOUT') {
         steps {
               cleanWs()  
               checkout scm
         }
      }

      stage('Execute CodeBuild projects in AWS') {
         steps {

            // echo 'Parse yaml file with python3 script and output codebuild projects in txt file...'
            // sh 'python3 parse_yaml.py'

            // echo 'Execute codebuild projects...'
            // sh 'bash execute_codebuild_projects.sh'

            echo 'Parse yaml and execute CodeBuild Projects...'
            sh 'python3 -u execute_codebuild_from_yaml.py'
         }
      }

   }
}
