# This Dev dockerfile requires pre-built .mar models inside folder /model-store
# to avoid the need of downloading models on every build.
#
# To build .mar models check build_mar_example.sh.
#
# model_name should be "en", "pt_br" or "multilang".
#

FROM pytorch/torchserve:latest
# FROM pytorch/torchserve:0.5.1-gpu

ENV WORKDIR /home/model-server

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV LC_LANG C.UTF-8

RUN python3 -m pip install --upgrade pip

COPY model-assets/. ${WORKDIR}
COPY model-store ${WORKDIR}/model-store

CMD ["torchserve", "--start", "--model-store", "model-store"]

# Instead of config.properties, load_models could be passed dinamically as:
# CMD ["torchserve", "--start", "--model-store", "model-store", "--models", "pt_br=pt_br.mar"]
