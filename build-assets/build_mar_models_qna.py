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
        print('model', model)
        print('model_name', model_name)
        print('model_version', model_version)
        
        # the model must be unzip before an be located at root folder in this way: models/MODEL_NAME
        try:
            files = os.listdir(os.path.join('models', model_name))
        except:
            print("Can't find directory or files inside models/MODEL_NAME")
        os.mkdir(os.path.join('models', model_name, 'extra_files'))
        #print(os.path.join('models', model_name))

        for file in files:
            if not file.endswith('.bin'):  # move all files except .bin to extra_files folder
                shutil.move(
                    os.path.join('models', model_name, file),
                    os.path.join('models', model_name, 'extra_files', file)
                )
        
        print('pwd', os.getcwd())
        
        if model_name == 'qna2':
            os.system(f'./build_mar_qna.sh -n {model_name} -f {model_name} -v {model_version} -o {output_dir}')
        else:
            os.system(f'./build_mar.sh -n {model_name} -f {model_name} -v {model_version} -o {output_dir}')

    #shutil.rmtree('models')  # delete folder models after build all .mar


if __name__ == "__main__":
    """
    Builds a .mar model for every model in models folder,
    then delete models folder
    
    argv[1] : str: 'model1_name:model1_version=URL1|model2_name:model2_version=URL2|...'
    argv[2] : str: WORKDIR
    """
    plac.call(build_mar_models, sys.argv[1:])
