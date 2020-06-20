#!/bin/bash

file_name="codebuild_projects.txt"

# iterate over codebuild projects and execute commands
while read line; do

echo $line  

# start CodeBuild project
aws codebuild start-build --project-name $line

done < $file_name

