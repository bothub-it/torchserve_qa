import plac
import sys
import os
import shutil


def build_mar_models(*args):
    os.chdir(args[1])

    output_dir = 'model-store'
    os.makedirs(output_dir, exist_ok=True)  # target output folder

    models = args[0].split('|')
    for model_info in models:
        model, _ = model_info.split("=")
        model_name, model_version = model.split(":")

        files = os.listdir(os.path.join('models', model_name))
        os.mkdir(os.path.join('models', model_name, 'extra_files'))

        for file in files:
            if not file.endswith('.bin'):  # move all files except .bin to extra_files folder
                os.rename(
                    os.path.join('models', model_name, file),
                    os.path.join('models', model_name, 'extra_files', file)
                )

        os.system(f'./build_mar.sh -n {model_name} -f {model_name} -v {model_version} -o {output_dir}')

    shutil.rmtree('models')  # delete folder models after build all .mar


if __name__ == "__main__":
    """
    Builds a .mar model for every model in models folder,
    then delete models folder
    
    argv[1] : str: 'model1_name:model1_version=URL1|model2_name:model2_version=URL2|...'
    argv[2] : str: WORKDIR
    """
    plac.call(build_mar_models, sys.argv[1:])
