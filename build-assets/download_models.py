import logging
import plac
import os
import requests
import sys
import zipfile
import urllib.request 
import shutil

logger = logging.getLogger(__name__)


def download_file(url, file_name):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(file_name, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return file_name


def download_models(*args):
    
    models = args[0].split("|")
    workdir = args[1]
    workdir_qna2 = os.path.join(workdir, 'model-store')
    download_file('https://bothub-nlp-models.s3.amazonaws.com/qa-2/qna2.mar', 'qna2.mar')
    if not os.path.isdir(workdir_qna2):
        os.mkdir(workdir_qna2)
    shutil.move("qna2.mar",os.path.join(workdir_qna2, 'qna2.mar'))
    for model_info in models:
        model, url = model_info.split("=")
        model_name, version = model.split(":")
        file_name = 'zipped_model.zip'
        logger.info(f"downloading model {model_name} {version}. . .")
        download_file(url, file_name)
        logger.info(f"extracting model {model_name} {version}. . .")
        with zipfile.ZipFile(file_name, 'r') as zip_ref:
            zip_ref.extractall(os.path.join(workdir, 'models'))
        os.remove(file_name)


if __name__ == "__main__":
    """
    Downloads and extract one or more zipped models
    argv[1] : str: 'model1_name:model1_version=URL1|model2_name:model2_version=URL2|...'
    argv[2] : str: Extract path
    """
    plac.call(download_models, sys.argv[1:])
