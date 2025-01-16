#FROM pytorch/pytorch:2.4.0-cuda11.8-cudnn9-runtime
FROM python:3.9-slim

ARG NAME
ARG NLP_CONF_FILE=presidio_analyzer/conf/transformers.yaml
ARG ANALYZER_CONF_FILE=presidio_analyzer/conf/default_analyzer.yaml
ARG RECOGNIZER_REGISTRY_CONF_FILE=presidio_analyzer/conf/default_recognizers.yaml
ENV PIP_NO_CACHE_DIR=1
ENV CUDA_VISIBLE_DEVICES=-1

WORKDIR /usr/bin/${NAME}

ENV ANALYZER_CONF_FILE=${ANALYZER_CONF_FILE}
ENV RECOGNIZER_REGISTRY_CONF_FILE=${RECOGNIZER_REGISTRY_CONF_FILE}
ENV NLP_CONF_FILE=${NLP_CONF_FILE}
ENV HF_HOME=./.cache
ENV STANZA_RESOURCES_DIR=./.cache/stanza

COPY ${ANALYZER_CONF_FILE} /usr/bin/${NAME}/${ANALYZER_CONF_FILE}
COPY ${RECOGNIZER_REGISTRY_CONF_FILE} /usr/bin/${NAME}/${RECOGNIZER_REGISTRY_CONF_FILE}
COPY ${NLP_CONF_FILE} /usr/bin/${NAME}/${NLP_CONF_FILE}

COPY ./requirements.txt .

RUN apt-get update && apt-get install -y build-essential curl

# next line is required to install the CPU version of Torch and not the GPU one, see
# https://pytorch.org/get-started/locally/
RUN pip install uv==0.2.2
ENV VIRTUAL_ENV=/usr/local
RUN uv pip sync requirements.txt --python=/usr/local/bin/python  && uv cache clean
RUN pip install torch --index-url https://download.pytorch.org/whl/cpu

COPY . .

RUN python install_nlp_models.py --conf_file ${NLP_CONF_FILE}

EXPOSE ${PORT}
CMD python app_presidio.py --host 0.0.0.0
