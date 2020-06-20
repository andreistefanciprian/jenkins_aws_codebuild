pipeline {
   agent any
    environment {
        AWS_ACCESS_KEY_ID = credentials('aws_access_key')
        AWS_REGION = credentials('aws_region')
        AWS_DEFAULT_REGION = credentials('aws_region')
        AWS_SECRET_ACCESS_KEY = credentials('aws_secret_key')
    }
   stages {
      stage('Hello') {
         steps {
            echo 'issue AWS commands'
            sh 'aws codebuild list-projects'
            // sh 'aws codebuild start-build --project-name codebuildtest-MessageUtil'

            // generate txt file with codebuild projects
            sh 'python3 parse_yaml.py'
            sh 'ls -larth'
            sh 'cat codebuild_projects.txt'

            // execute codebuild projects
            sh 'bash execute_codebuild_projects.sh'
         }
      }
   }
}
