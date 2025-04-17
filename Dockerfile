FROM nvidia/cuda:12.6.1-runtime-ubuntu20.04
WORKDIR /t-lite

RUN apt-get update && \
    apt-get install -y python3-pip python3 && \
    rm -rf /var/lib/apt/lists/*
RUN pip install uv

COPY pyproject.toml uv.lock .
RUN uv sync --frozen

COPY . .
CMD [ "uv", "run", "python", "-m", "src.app"]
