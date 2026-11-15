FROM python:3.12-slim AS builder

RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build
COPY requirements.txt ./
RUN pip install --no-cache-dir --disable-pip-version-check --prefix=/install -r requirements.txt

FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    BALNEABILIDADE_CACHE_DIR=/tmp/balneabilidade

COPY --from=builder /install/ /usr/local/
WORKDIR /app

EXPOSE 8000
CMD ["balneabilidade-sc-mcp-http"]
