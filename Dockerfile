FROM pytorch/torchserve:latest

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV LC_LANG C.UTF-8

RUN python3 -m pip install --upgrade pip

CMD ["torchserve", "--start", "--model-store", "model-store", "--models", "QA_pt-br=QA_pt-br.mar", "--ts-config", "model-store/config.properties"]
# CMD ["torchserve","--start","--model-store","$MODEL_BASE_PATH/torchserve","--models","densenet161.mar","--ts-config","$MODEL_BASE_PATH/torchserve/config.properties"]
