# Requires ARG DOWNLOAD_MODELS (urls of zipped models to download)
# ie.: DOWNLOAD_MODELS="model1_name:model1_version=URL1|model2_name:model2_version=URL2|..."
#
# The URLs must contain zipped files formatted as <any_name.zip/model_name/.>
# to be properly processed
#
# config.properties file must be adapted to suit model name and configs
#

FROM pytorch/torchserve:latest
# FROM pytorch/torchserve:0.5.1-gpu

ENV WORKDIR /home/model-server

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV LC_LANG C.UTF-8

USER root

COPY build-assets/. ${WORKDIR}
RUN python3 -m pip install --upgrade pip
RUN pip3 install -r build_requirements.txt

COPY model-assets/. ${WORKDIR}

ARG DOWNLOAD_MODELS

RUN if [ ${DOWNLOAD_MODELS} ]; then \
        python3 download_models.py ${DOWNLOAD_MODELS} ${WORKDIR} && \
        python3 build_mar_models.py ${DOWNLOAD_MODELS} ${WORKDIR}; \
    fi

USER model-server

CMD ["torchserve", "--start", "--model-store", "model-store"]

