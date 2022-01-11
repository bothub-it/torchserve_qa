# Torchserve QA model prototype


## About

First, models need to be processed to .mar extension using `torch-model-archiver` utility
- see _build_mar.sh_ for example

Processed .mar models must be at **/model-store** directory

## Build and run
### Using docker-compose
Run `docker-compose up --build` to build and run
### Manually
Run `docker build -t torchserve_prototype:latest .` to build

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
To work properly, the GPU should be compatible with CUDA 10.2 and the same version should be installed in the running machine. 

_(CUDA 10.2 is, for now, the default CUDA version installed in torchserve base images)_

If the GPU is not compatible with this CUDA version, you can build yourself the Torchserve image with a custom CUDA version following the steps at https://github.com/pytorch/serve/tree/master/docker 

## Application access to models
There are two ways to use the models in the application (we're still deciding how it's going to work at production environment)
- (Default) Send models to the image at Build time - /model-store folder is copied to the image at build time, as you can see in Dockerfile:
````
COPY model-store ${WORKDIR}/model-store
````

- Another option is to access model from the container volume during runtime - A volume can be created at runtime which the container can access. Example:
````
docker run --rm -it \
-p 8080:8080 -p 8081:8081 -p 8082:8082 \
-v $(pwd)/model-store:/home/model-server/model-store torchserve_prototype:latest 
````

## Testing endpoints

Endpoint status:

`curl -X GET http://localhost:8080/ping`

Inference example:

`curl http://localhost:8080/predictions/QA_pt-br -T test.json`

See more at:

https://pytorch.org/serve/inference_api.html
