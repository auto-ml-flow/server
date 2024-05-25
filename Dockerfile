FROM python:3.12 as builder

ENV PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

RUN apt update
# musl-dev is "general" c compiler necessary
RUN apt install musl-dev libpq-dev gcc -y

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .

RUN pip install -r requirements.txt

FROM python:3.12-slim-bookworm

RUN apt update
RUN apt install libpq-dev -y

COPY --from=builder /opt/venv /opt/venv

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH"

WORKDIR /app

ADD . .
