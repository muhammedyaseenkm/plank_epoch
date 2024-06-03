FROM python:3.7-slim

LABEL maintainer="MCV & murat@visiosoft.com.tr"

ENV DOCKER=true

COPY pyproject.toml .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir poetry && \
    poetry install

EXPOSE 8000