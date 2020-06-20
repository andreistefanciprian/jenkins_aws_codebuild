

import yaml
import os


def parse_yaml(file_path):
    """
    Parse yaml file and output codebuild steps in txt file.
    """

    result = False

    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            try:
                read_yaml = yaml.full_load(file)
            except Exception as e:
                raise e
            else:
                for codebuild_project in read_yaml['codebuild_projects']:
                    # write to file
                    with open('codebuild_projects.txt', 'a+') as file:
                         file.write(codebuild_project + '\n')
                        # print(codebuild_project)
                result = True
            finally:
                return result
    else:
        result = f"File/Directory {file_path} does not exist!"
        return result
    
# tests
file_path = 'file.yaml'
parse = parse_yaml(file_path)
print(parse)