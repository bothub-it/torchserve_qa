#!/bin/bash
torch-model-archiver --model-name pt_br \
--version 1.0 \
--serialized-file pt_br/pytorch_model.bin \
--export-path ./model-store -f \
--handler model-assets/ModelHandler.py \
--extra-files pt_br/extra_files \
-r model-assets/requirements.txt
