#!/bin/bash
torch-model-archiver --model-name QA_pt-br \
--version 1.0 \
--serialized-file pt_br/pytorch_model.bin \
--export-path ./model-store -f \
--handler ModelHandler.py \
--extra-files pt_br/extra_files \
-r requirements.txt
