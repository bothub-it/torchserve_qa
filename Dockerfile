# Requires --build-arg DOWNLOAD_MODELS="model1_name:model1_version=URL1|model2_name:model2_version=URL2|..."
# eg.: DOWNLOAD_MODELS="pt_br:1.0=http://modelurl.com/pt_br|en:1.0=http://modelurl.com/en"
#
# The URLs must contain zipped files formatted as <any_name.zip/model_name/files_here>
# to be properly processed.
#
# model_name should be "en", "pt_br" or "multilang".
#

# FROM pytorch/torchserve:latest
FROM pytorch/torchserve:0.5.1-gpu

ENV WORKDIR /home/model-server

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV LC_LANG C.UTF-8

USER root

COPY build-assets/. ${WORKDIR}
RUN python3 -m pip install --upgrade pip
RUN pip3 install -r build_requirements.txt

COPY model-assets/. ${WORKDIR}

COPY dockerd-entrypoint.sh /usr/local/bin/
RUN chown -Rv model-server /home/model-server/model-store

ARG DOWNLOAD_MODELS

USER model-server

RUN if [ ${DOWNLOAD_MODELS} ]; then \
        python3 download_models.py ${DOWNLOAD_MODELS} ${WORKDIR} && \
        python3 build_mar_models.py ${DOWNLOAD_MODELS} ${WORKDIR}; \
    fi

CMD ["serve"]

