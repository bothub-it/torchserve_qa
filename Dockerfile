# FROM pytorch/torchserve:latest
FROM pytorch/torchserve:0.5.1-gpu

ENV WORKDIR /home/model-server

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV LC_LANG C.UTF-8

RUN python3 -m pip install --upgrade pip

COPY model-store ${WORKDIR}/model-store
COPY config.properties ${WORKDIR}

CMD ["torchserve", "--start", "--model-store", "model-store", "--models", "QA_pt-br=QA_pt-br.mar", "--ts-config", "config.properties"]
