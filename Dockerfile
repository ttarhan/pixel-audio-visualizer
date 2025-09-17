FROM python:3.13-bookworm

RUN apt update && \
    apt install -y portaudio19-dev libasound2-dev alsa-utils && \
    rm -rf /var/cache/apt/archives /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/install.sh | sh

ENV PATH="/root/.local/bin:${PATH}"

WORKDIR /app

COPY pyproject.toml uv.lock README.md LICENSE .
COPY visualizer/__init__.py visualizer/
RUN uv sync

COPY . .
RUN uv sync

ENV CAPTURE_GAIN=5

CMD ./run.sh