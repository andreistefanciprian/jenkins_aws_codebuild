import yaml
import os
import boto3
import json
import time

def execute_codebuild_from_yaml(yaml_file):
    """
    Execute AWS codebuild projects provided in yaml file.
    """
    if os.path.exists(yaml_file):
        with open(yaml_file, 'r') as file:
            try:
                read_yaml = yaml.full_load(file)
            except Exception as e:
                raise e
            else:
                client = boto3.client('codebuild')
                codebuild_projects = client.list_projects()
                codebuild_projects = codebuild_projects['projects']

                for codebuild_project in read_yaml['codebuild_projects']:
                    if codebuild_project in codebuild_projects:
                        client.start_build(projectName=codebuild_project)
                        # print(f"Started {get_last_build_results(client, codebuild_project)}")

                        # print results of last build
                        # last_build_results = get_last_build_results(client, codebuild_project)
                        # for k,v in last_build_results.items():
                        #     print(f"{k}: {v}")

                        # while last_build_results['Build Status'] == 'SUCCEEDED':
                        #     print(f'Build {last_build_results['Build Number']} of {last_build_results['Build Project Name']} is a success!')

                        # {'Build Number': 13, 'Build Start Time': datetime.datetime(2020, 6, 20, 14, 6, 46, 284000, tzinfo=tzlocal()), 'Build Status': 'IN_PROGRESS', 'Build Project Name': 'newproj-test'}
                        # status_msg = f"CodeBuild Project: {last_build_results['Build Project Name']} -- Build Number: {last_build_results['Build Number']} -- Status: {last_build_results['Build Status']}"
                        # print(status_msg)

                        while True:
                            last_build_results = get_last_build_results(client, codebuild_project)
                            status_msg = f"CodeBuild Project: {last_build_results['Build Project Name']} -- Build Number: {last_build_results['Build Number']} -- Status: {last_build_results['Build Status']}"

                            if last_build_results['Build Status'] == 'SUCCEEDED':
                                # print(f"Build {last_build_results['Build Number']} {last_build_results['Build Status']}")
                                print(status_msg)
                                break
                            else:
                                # print(f"Build {last_build_results['Build Number']} {last_build_results['Build Status']}")
                                print(status_msg)
                                time.sleep(10)
                                continue
                        
                        # display build run result in json format
                        # build_result = dict2json(build_data)
                        # print(build_result)


                    else:
                        print(f"{codebuild_project} is not available in AWS CodeBuild Project list.")

    else:
        result = f"{yaml_file} file does not exist!"
        return result

def get_last_build_results(client, codebuild_project):
    """
    Get CodeBuild result of last build.
    """
    build_result = {}

    project_builds = client.list_builds_for_project(projectName=codebuild_project)
    build_id = project_builds['ids'][0]
    build_data = client.batch_get_builds(ids = [build_id])
    
    build_result['Build Number'] = build_data['builds'][0]['buildNumber']
    build_result['Build Start Time'] = build_data['builds'][0]['startTime']
    build_result['Build Status'] = build_data['builds'][0]['buildStatus']
    build_result['Build Project Name'] = build_data['builds'][0]['projectName']

    return build_result



def dict2json(data: dict):
    """
    Parse CodeBuild build result from dict to nice JSON output.
    """
    build_data_json = json.dumps(data, indent=4, sort_keys=True, default=str)
    parsed = json.loads(str(build_data_json))
    return json.dumps(parsed, indent=4, sort_keys=True)


if __name__ == "__main__":
    
    # variables
    yaml_file = os.path.join(os.getcwd(), 'file.yaml')

    # execute codebuild projects
    execute_codebuild_from_yaml(yaml_file)
