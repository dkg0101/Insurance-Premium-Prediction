import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)

project_name = 'insurance'

list_of_files = [
    f"src/{project_name}/__init__.py",
    f"src/{project_name}/components/__init__.py",
    f"src/{project_name}/components/data_ingestion.py",
    f"src/{project_name}/components/data_validation.py",
    f"src/{project_name}/components/data_transformation.py",
    f"src/{project_name}/components/model_trainer.py",
    f"src/{project_name}/components/model_evaluation.py",
    f"src/{project_name}/components/model_pusher.py",
    f"src/{project_name}/constant/__init__.py",
    f"src/{project_name}/configuration/__init__.py",
    f"src/{project_name}/data_access/__init__.py",
    f"src/{project_name}/entity/__init__.py",
    f"src/{project_name}/pipeline/__init__.py",
    f"src/{project_name}/utils/__init__.py",
    f"src/{project_name}/exception.py",
    f"src/{project_name}/logger.py",
    "main.py",
    "app.py",
    ".github/workflows/.gitkeep",
    "Dockerfile"

]

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir,filename= os.path.split(filepath)

    if filedir != '':
        os.makedirs(filedir,exist_ok=True)
        logging.info(f"Creating directory:{filedir} for file:{filename}")

    
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath,'w') as f:
            pass
            logging.info(f"Creating empty file: {filepath}")
    else:
        logging.info(f"{filename} is already exists")

