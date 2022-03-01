FROM python:3.8.8-slim-buster
WORKDIR /usr/src/app
ENV PYTHONFAULTHANDLER=1
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt
RUN echo 'alias jlab="jupyter lab --allow-root --ip 0.0.0.0 --no-browser"' >> ~/.bashrc
RUN echo 'alias tst="python -m pytest orp/content_enrichment/test"' >> ~/.bashrc
RUN echo 'alias ntst="python -m pytest orp/authority_ner/"' >> ~/.bashrc
