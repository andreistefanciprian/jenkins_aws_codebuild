import yaml
import os
import boto3
from boto3.session import Session
import json
import time
import sys
import datetime

def main(codebuild_list, **kwargs):
    """
    Execute AWS codebuild projects.
    """

    # assume AWS Role and get list of configured AWS CodeBuild projects
    session = AwsSession(**kwargs)
    codebuild_projects_in_aws = session.get_codebuild_projects()

    # parse yaml file and start CodeBuild projects
    for codebuild_project in codebuild_list:

        # verify if codebuild project in yaml file available in AWS
        if codebuild_project in codebuild_projects_in_aws:
    
            # assume AWS Role and start CodeBuild project build
            session = AwsSession(**kwargs)
            session.start_codebuild_build(codebuild_project)
    
            # verify CodeBuild build status
            status = session.get_codebuild_status(codebuild_project)
            if status != 'SUCCEEDED':
                sys.exit(f'CodeBuild Project {codebuild_project} failed!')
        else:
            log(f'{codebuild_project} is not available in AWS CodeBuild Project list.', warn=True)

def log(message, new_line=False, green=False, warn=False):
    """
    Print message to stdout with timestamp.
    """
    ENDC = '\033[0m'
    OKGREEN = '\033[32;1m'
    FAIL = '\033[31;1m'

    now = datetime.datetime.now().strftime('%H:%M:%S')
    if new_line:
        print('\n' + now, message)
    elif green:
        print('\n' + f'{OKGREEN}{now} {message}{ENDC}')
    elif warn:
        print('\n' + f'{FAIL}{now} {message}{ENDC}')
    else:
        print(now, message)

def parse_yaml(yaml_file, yaml_list_elem):
    """
    Parse yaml file and return a list of CodeBuild projects to execute in AWS.
    return: list
    """

    cb_projects_to_run = []

    if os.path.exists(yaml_file):
        log(f'Reading {yaml_file} file ...', green=True)
        with open(yaml_file, 'r') as file:
            try:
                read_yaml = yaml.full_load(file)
            except Exception as e:
                log(str(e))
                raise
            else:
                cb_projects_to_run = read_yaml[yaml_list_elem]
                log(f'CodeBuild projects to run are:', green=True)
                for cb_project in cb_projects_to_run:
                    print(cb_project)
                return cb_projects_to_run
    else:
        raise(f'{yaml_file} file does not exist!')
    
            
class AwsSession:

    """
    Assume IAM Role.
    Establish AWS Session with assumed IAM role.
    Sending commands to AWS.
    """

    def __init__(self, aws_account, aws_iam_role, aws_region, sts_duration=None, sts_external_id=None, sts_session_name=None, logs_group_name=None):

        # aws instance vars
        self.aws_account = aws_account
        self.aws_iam_role = aws_iam_role
        self.arn = f'arn:aws:iam::{aws_account}:role/{aws_iam_role}'
        self.sts_session_name = 'jenkins_session' if sts_session_name is None else sts_session_name
        self.aws_region = aws_region

        # aws assume role instance vars
        self.sts_external_id = 'jenkins_id' if sts_external_id is None else sts_external_id
        self.sts_duration = 3600 if sts_duration is None else sts_duration
        self._sts_client = None
        self._sts_session = self._assume_role()

        # aws codebuild instance vars
        self._codebuild_client = None
        self.codebuild_projects = None
        self._codebuild_is_connected = False
        self.sts_caller_identity = self._get_sts_caller_identity()
        
        # aws cloudwatch instance vars
        self.logs_group_name = 'cw-cb-group' if logs_group_name is None else logs_group_name
        self.codebuild_id = None
        self._logs_client = None
        self._logs_is_connected = False
        self._logs_stream_id = None

    def _assume_role(self):
        """
        Assume AWS IAM Role.
        """

        try:
            self._sts_client = boto3.client('sts')
        except Exception as e:
            log(str(e))
            raise
        else:
            response = self._sts_client .assume_role(RoleArn=self.arn, RoleSessionName=self.sts_session_name, DurationSeconds=self.sts_duration, ExternalId=self.sts_external_id)

            session = Session(aws_access_key_id=response['Credentials']['AccessKeyId'],
                        aws_secret_access_key=response['Credentials']['SecretAccessKey'],
                        aws_session_token=response['Credentials']['SessionToken'],
                        region_name=self.aws_region)
            return session

    def _get_sts_caller_identity(self):
        """
        Returns details about the IAM user or role whose credentials are used to call the operation.
        return: dict
        """

        try:
            client = self._sts_session.client('sts')
        except Exception as e:
            log(str(e))
            raise
        else:
            caller_identity = client.get_caller_identity()
            log("STS Identity assumed!", green=True)
            for k,v in caller_identity.items():
                    print(k,v)
            return caller_identity

    def _cwlogs_client(self):
        """
        Create a low-level service Cloudwatch client by name.
        return: True or False
        """

        if not self._logs_is_connected:
            try:
                self._logs_client = self._sts_session.client('logs')
            except Exception as e:
                log(str(e))
                raise
            else:
                self._logs_is_connected = True
                return self._logs_is_connected
        else:
            return self._logs_is_connected

    def _cb_client(self):
        """
        Create a low-level service CodeBuild client by name.
        return: True or False
        """

        if not self._codebuild_is_connected:
            try:
                self._codebuild_client = self._sts_session.client('codebuild')
            except Exception as e:
                log(str(e))
                raise
            else:
                self._codebuild_is_connected = True
                return self._codebuild_is_connected
        else:
            return self._codebuild_is_connected

    def display_cloudwatch_logs(self):
        """
        Get CloudWatch logs from AWS.
        return: Prints the logs
        """ 

        if self._cwlogs_client():

            log_stream_id = self.codebuild_id.split(':')[1]
            codebuild_project = self.codebuild_id.split(':')[0]
            log_stream = f'{codebuild_project}/{log_stream_id}'

            try:
                response = self._logs_client.get_log_events(
                    logGroupName=self.logs_group_name,
                    logStreamName=log_stream,
                    startFromHead=True
                )
            except Exception as e:
                log(str(e))
                raise
            else:
                log(f'Cloudwatch logs for {self.codebuild_id}:', new_line=False)
                for i in response['events']:
                    msg = i['message'].strip()
                    print(msg)
        else:
            raise Exception('Cannot establish CloudWatch connection ...!')

    def get_codebuild_projects(self):
        """
        Get list of CodeBuild projects from AWS.
        return: list of projects
        """ 

        if self._cb_client():
            try:
                self.codebuild_projects = self._codebuild_client.list_projects()
            except Exception as e:
                log(str(e))
                raise
            else:
                log('CodeBuild projects currently available in AWS:', green=True)
                for project in self.codebuild_projects['projects']:
                    print(project)
                return self.codebuild_projects['projects']
        else:
            raise Exception('Cannot establish CodeBuild connection ...!')

    def get_codebuild_build_result(self, codebuild_project):
        """
        Get CodeBuild result of last build.
        return: dictionary
        """

        if self._cb_client():
            result = {}

            try:
                build_data = self._codebuild_client.batch_get_builds(ids = [self.codebuild_id])
            except Exception as e:
                log(str(e))
                raise
            else: 
                result['Build Number'] = build_data['builds'][0]['buildNumber']
                result['Build Start Time'] = build_data['builds'][0]['startTime']
                result['Build Status'] = build_data['builds'][0]['buildStatus']
                result['Build Project Name'] = build_data['builds'][0]['projectName']
            return result
        else:
            raise Exception("Cannot establish CodeBuild connection ...")

    def start_codebuild_build(self, codebuild_project):
        """
        Start CodeBuild project build.
        """

        if self._cb_client():
            try:
                result = self._codebuild_client.start_build(projectName=codebuild_project)
            except Exception as e:
                log(str(e))
                raise
            else:
                self.codebuild_id = result['build']['id']
                build_number = result['build']['buildNumber']
                build_start_time = (result['build']['startTime']).strftime("%H:%M:%S")
                log(f"Started build {build_number}, {self.codebuild_id} at {build_start_time} ...", green=True)
        else:
            raise Exception('Cannot establish CodeBuild connection ...!')

    def get_codebuild_status(self, codebuild_project):
        """
        This function verifies the status of the last CodeBuild build until it is successfull.
        return: string (IN_PROGRESS, SUCCEEDED, FAILED, etc)
        """

        time_interval = 15   # verify status every n seconds
        time_left = 3600     # max time a build can take in seconds
        result = 'FAIL'

        while time_left > 0:
            
            time_left -= time_interval

            try:
                last_build_results = self.get_codebuild_build_result(codebuild_project)
            except Exception as e:
                log(str(e))
                raise
            else:
                codebuild_project = last_build_results['Build Project Name']
                codebuild_build_number = last_build_results['Build Number']
                codebuild_status = last_build_results['Build Status']
                status_msg = f'CodeBuild Project {codebuild_project} build {codebuild_build_number}: {codebuild_status}'

                if last_build_results['Build Status'] == 'IN_PROGRESS':
                    log(status_msg)
                    time.sleep(time_interval)
                    result = last_build_results['Build Status']
                    continue
                elif last_build_results['Build Status'] == 'SUCCEEDED':
                    log(status_msg)
                    result = last_build_results['Build Status']
                    self.display_cloudwatch_logs()
                    break
                else:
                    log(status_msg)
                    result = last_build_results['Build Status']
                    self.display_cloudwatch_logs()
                    break

        return result


if __name__ == "__main__":

    # define vars
    yaml_file = os.path.join(os.getcwd(), 'codebuild_projects.yaml')
    aws_account = sys.argv[1] if len(sys.argv) == 2 else sys.exit('AWS ARN Role has to be provided as positional parameter!')
    aws_iam_role = 'tf_role'
    aws_region = 'us-east-1'
    sts_session_name = 'funky_test'
    sts_external_id = 'smth'
    sts_duration = 3600
    
    # parse yaml file
    codebuild_projects_from_yaml = parse_yaml(yaml_file, 'codebuild_projects')

    # execute codebuild projects
    main(codebuild_projects_from_yaml, aws_account=aws_account, aws_iam_role=aws_iam_role, sts_session_name=sts_session_name, aws_region=aws_region, sts_external_id=sts_external_id, sts_duration=sts_duration)
    # main(codebuild_projects_from_yaml, aws_account=aws_account, aws_iam_role=aws_iam_role, aws_region=aws_region, sts_session_name=sts_session_name)
    
