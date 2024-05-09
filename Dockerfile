FROM python:3.12-alpine as builder

ENV PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

RUN apk update
# musl-dev is "general" c compiler necessary
RUN apk add musl-dev libpq-dev gcc

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .

RUN pip install -r requirements.txt

FROM python:3.12-alpine

RUN apk update
RUN apk add libpq-dev

COPY --from=builder /opt/venv /opt/venv

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH"

WORKDIR /app

ADD . .
