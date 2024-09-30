FROM python:3.12-bookworm

RUN apt update && \
    apt install -y portaudio19-dev libasound2-dev alsa-utils && \
    rm -rf /var/cache/apt/archives /var/lib/apt/lists/*

RUN pip install --user pdm

ENV PATH="$PATH:/root/.local/bin"

WORKDIR /app

COPY pyproject.toml pdm.lock README.md LICENSE .

RUN pdm install

COPY * .

ENV PA_MIN_LATENCY_MSEC=4
ENV CAPTURE_GAIN=5

CMD ./run.sh