import yaml
import os
import boto3
from boto3.session import Session
import json
import time
import sys

def main(yaml_file, arn, session_name):
    """
    Execute AWS codebuild projects provided in yaml file.
    """

    if os.path.exists(yaml_file):
        with open(yaml_file, 'r') as file:
            try:
                read_yaml = yaml.full_load(file)
                print(f"Reading yaml file at: {yaml_file}")
            except Exception as e:
                print(str(e))
                raise e
            else:

                # assume AWS Role
                aws_role_session = assume_role(arn, session_name)
                client = aws_role_session.client('sts')

                # get current assumed role UserId
                account_id = client.get_caller_identity()["UserId"]
                print(f"\nCurrent Assumed AWS IAM User: {account_id}")

                print("\nConnecting to AWS to execute the CodeBuild projects...")
                client = aws_role_session.client('codebuild')
             
                # get list of CodeBuild projects from AWS
                codebuild_projects = get_codebuild_projects_from_aws(client)

                for codebuild_project in read_yaml['codebuild_projects']:
                    if codebuild_project in codebuild_projects:
                        print(f"\nCodeBuild Project {codebuild_project} is available in AWS CodeBuild Project list.")
                        
                        # start CodeBuild project build
                        start_build(client, codebuild_project)

                        # verify CodeBuild build status
                        status = verify_build_status(client, codebuild_project)
                        if status != "SUCCEEDED":
                            msg = f"CodeBuild Project {codebuild_project} failed!"
                            print(msg)
                            sys.exit(1)
                        else:
                            msg = f"CodeBuild Project {codebuild_project}: {status}!"
                            print(msg)
                            continue

                    else:
                        print(f"\n{codebuild_project} is not available in AWS CodeBuild Project list.")

    else:
        result = f"{yaml_file} file does not exist!"
        print(result)

def assume_role(arn, session_name):
    """
    Assume AWS IAM Role.
    """

    try:
        client = boto3.client('sts')
    except Exception as e:
        print(str(e))
        raise e
    else:
        response = client.assume_role(RoleArn=arn, RoleSessionName=session_name)
        session = Session(aws_access_key_id=response['Credentials']['AccessKeyId'], aws_secret_access_key=response['Credentials']['SecretAccessKey'], aws_session_token=response['Credentials']['SessionToken'])
    
        return session

def get_codebuild_projects_from_aws(client):
    """
    Get list of CodeBuild projects from AWS.
    Returns a list of projects.
    """
    
    try:
        codebuild_projects = client.list_projects()
    except Exception as e:
        print(str(e))
        raise e
    else:
        return codebuild_projects['projects']

def start_build(client, codebuild_project):
    """
    Start CodeBuild project build.
    """
    try:
        client.start_build(projectName=codebuild_project)
    except Exception as e:
        print(str(e))
        raise e
    else:
        last_build_results = get_last_build_results(client, codebuild_project)
        print(f"Started build {last_build_results['Build Number']} for the AWS CodeBuild Project {codebuild_project} at {last_build_results['Build Start Time']} ...")

def verify_build_status(client, codebuild_project):
    """
    This function verifies the status of the last CodeBuild build until it is successfull.
    """

    time_interval = 5   # verify status every n seconds
    time_left = 300     # max time a build can take in seconds
    result = "FAIL"

    while time_left > 0:
        
        time_left -= time_interval

        try:
            last_build_results = get_last_build_results(client, codebuild_project)
        except Exception as e:
            print(str(e))
            raise e
        else:
            codebuild_project = last_build_results['Build Project Name']
            codebuild_build_number = last_build_results['Build Number']
            codebuild_status = last_build_results['Build Status']
            status_msg = f"CodeBuild Project {codebuild_project} build {codebuild_build_number}: {codebuild_status}"

            if last_build_results['Build Status'] == 'IN_PROGRESS':
                print(status_msg)
                time.sleep(time_interval)
                result = last_build_results['Build Status']
                continue
            elif last_build_results['Build Status'] == 'SUCCEEDED':
                print(status_msg)
                result = last_build_results['Build Status']
                break
            else:
                print(status_msg)
                result = last_build_results['Build Status']
                break

    return result

def get_last_build_results(client, codebuild_project):
    """
    Get CodeBuild result of last build.

    Return dictionary.
    """

    result = {}

    try:
        project_builds = client.list_builds_for_project(projectName=codebuild_project)
    except Exception as e:
        print(str(e))
        raise e
    else: 
        build_id = project_builds['ids'][0]
        build_data = client.batch_get_builds(ids = [build_id])
        result['Build Number'] = build_data['builds'][0]['buildNumber']
        result['Build Start Time'] = build_data['builds'][0]['startTime']
        result['Build Status'] = build_data['builds'][0]['buildStatus']
        result['Build Project Name'] = build_data['builds'][0]['projectName']
        return result

def dict2json(data: dict):
    """
    Parse CodeBuild build result from dict to nice JSON output.
    """

    build_data_json = json.dumps(data, indent=4, sort_keys=True, default=str)
    parsed = json.loads(str(build_data_json))
    return json.dumps(parsed, indent=4, sort_keys=True)


if __name__ == "__main__":

    # define vars
    arn = sys.argv[1] if len(sys.argv) == 2 else sys.exit("AWS ARN Role has to be provided as positional parameter!")
    yaml_file = os.path.join(os.getcwd(), 'codebuild_projects.yaml')
    session_name = "funky_test"

    # execute codebuild projects in yaml file
    main(yaml_file, arn, session_name)
