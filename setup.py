from setuptools import find_packages, setup
from typing import List

HYPHEN_E_DOT='-e .'
# takes packages one by one from requirements.txt and returns it as a list
def get_requirements(file_path:str)->List[str]:
    requirements=[]
    with open(file_path) as file_obj:
        requirements=file_obj.readlines()
        requirements=[req.replace("\n","") for req in requirements]
        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)
    return requirements

# similar to metadata information of the entire project
setup(
    name='student-performance-indicator',
    version='0.0.1',
    author='Akash',
    author_email='akash.shantha@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')

)