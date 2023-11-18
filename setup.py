from setuptools import find_packages,setup
from typing import List

PROJECT_NAME='Insurance Premium Prediction'
VERSION = '0.0.1'
AUTHOR = 'Dhananjay Gurav'
AUTHOR_EMAIL = 'dkgurav0101@gmail.com'
DESCRIPTION = 'This project helps to predict medical expenses'
REQUIREMENT_FILE_NAME = "requirements.txt"
HYPEN_E_DOT = "-e ."

def get_requirements_list() -> List[str]:
    """
    Description: This function returns list of requirements for project
    mentioned in requirements.txt file

    """
    requirements = []
    with open(REQUIREMENT_FILE_NAME) as requirement_file:
        requirements = requirement_file.readlines()
        requirements =[req.replace('\n','') for req in requirements]

        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)
    
    return requirements


setup(
    name = PROJECT_NAME,
    version = VERSION,
    author = AUTHOR,
    author_email = AUTHOR_EMAIL,
    description = DESCRIPTION,
    packages = find_packages(),
    install_requires=get_requirements_list()
    )