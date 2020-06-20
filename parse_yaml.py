import yaml
import os

def parse_yaml(yaml_file, txt_file):
    """
    Parse yaml file and output AWS codebuild steps in txt file.
    """

    if os.path.exists(yaml_file):
        with open(yaml_file, 'r') as file:
            try:
                read_yaml = yaml.full_load(file)
            except Exception as e:
                raise e
            else:
                create_txt_file(txt_file)
                for codebuild_project in read_yaml['codebuild_projects']:
                    with open(txt_file, 'a+') as file:
                         file.write(codebuild_project + '\n')
            finally:
                with open(txt_file, 'r') as file:
                    result = file.read()
                    return result
    else:
        result = f"{yaml_file} file does not exist!"
        return result

def create_txt_file(txt_file):
    """
    Creates empty txt file.
    """
    with open(txt_file, 'w') as file:
        pass

if __name__ == "__main__":
    
    # variables
    txt_file = os.path.join(os.getcwd(), 'codebuild_projects.txt')
    yaml_file = os.path.join(os.getcwd(), 'file.yaml')

    #  execute function
    parse = parse_yaml(yaml_file, txt_file)
    print(parse)