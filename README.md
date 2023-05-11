# Torchserve QA model prototype

# Training and Generating .mar files
At the root project directory:
- python train.py your_csv_file.csv

- mv setup_config.json qna2/
- mkdir models/qna2
- cp qna2 models/
- cp build-assets/* .

- python build-assets/build_mar_models_qna.py qna2:1.0=none .

Save this file somewhere where you could user Curl command later.

Set QNA_MODEL env variable this .mar files generated.

# Development process (locally)
## Process models to .mar
Torchserve requires the models to be in .mar extension.

It can be done processing pytorch models `torch-model-archiver` utility.
- see _build_mar_example.sh_ for example

Built .mar models must be at **/model-store** directory to proceed.

## Build and run
### Using docker-compose
Run `docker-compose up --build` to build and run
### Manually
Run `docker build -f dev.Dockerfile -t torchserve_prototype:latest .` to build

Run container with:
````
docker run --rm -it \
-p 8080:8080 -p 8081:8081 -p 8082:8082 \
torchserve_prototype:latest
````

## Using GPUs

To run the model using GPU it is needed to run docker enabling the container to access machine gpus. You can use the command --gpus all, for example:
````
docker run --rm -it --gpus all \
-p 8080:8080 -p 8081:8081 -p 8082:8082 \
torchserve_prototype:latest
````
### Requirements
To work properly, the CUDA version should be the same at different levels:
- Pytorch version
- Docker image
- Local machine
- GPU

By default, for now, torchserve base image uses CUDA 10.2 inside, so, 
the GPU should be compatible with CUDA 10.2 and the same version should be installed in the running machine.

_Sometimes the exact same version is not required (there is compatibility in some versions), but its not recommended_

### Debug GPU compatibility
Run these commands to debug GPU compatibility, run them **outside the container and inside the container**:

_Remember the container must have access to the GPU outside using `--gpus all` command._

To check what version of CUDA is installed, run:

`nvidia-smi`

To check whether the application can access CUDA, run in the python interpreter:
````
import torch
torch.cuda.is_available()  # check if CUDA is available
torch.zeros(1).cuda()  # check if GPU is compatible with running CUDA
````

If the GPU is not compatible with this CUDA version (10.2), you can build yourself the 
Torchserve base image with a custom CUDA version following the steps at: https://github.com/pytorch/serve/tree/master/docker 

## Application access to models
There are two ways to use the models in the application
- (Default) Send models to the image at Build time - /model-store folder is copied to the image at build time, as you can see in Dockerfile:
````
COPY model-store ${WORKDIR}/model-store
````

- Another option is to access model from the container volume during runtime - A volume can be created at runtime which the container can access. Example:
````
docker run --rm -it \
-p 8080:8080 -p 8081:8081 -p 8082:8082 \
-v $(pwd)/model-store:/home/model-server/model-store \
torchserve_prototype:latest 
````

## Testing endpoints

Endpoint status:

`curl -X GET http://localhost:8080/ping`

Inference example:

`curl http://localhost:8080/predictions/pt_br -T request_example.json`

See more at:

https://pytorch.org/serve/inference_api.html

# Continuous Integration (production)

The main `Dockerfile` automatically do the steps mentioned above:
- Download models at buildtime
- Process models to .mar extension

## How to
`Dockerfile` expects the build-arg `DOWNLOAD_MODELS` containing **model name**, **version**, and **download url containing a zipped pytorch model**.

`DOWNLOAD_MODELS` should be formatted as:
`"model1_name:model1_version=URL1|model2_name:model2_version=URL2|..."`

Example:
````
docker build --build-arg DOWNLOAD_MODELS="pt_br:1.0=http://modelurl.com/pt_br|en:1.0=http://modelurl.com/en" \
-t torchserve_prototype:latest .
````
### Requirements
- _The zipped pytorch model from URL must be formatted as `any_name.zip/model_name/model_files_here`_
- _Model names must be, for now, `pt_br`, `en` or `multilang`_
