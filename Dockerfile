FROM nvidia/cuda:12.6.1-devel-ubuntu20.04

WORKDIR /tlite

RUN apt-get update && \
    apt-get install -y python3-pip git&& \
    rm -rf /var/lib/apt/lists/*

RUN pip install uv setuptools
COPY .python-version .
RUN uv python install

COPY pyproject.toml uv.lock .
RUN uv sync --frozen
RUN uv pip install "git+https://github.com/Dao-AILab/flash-attention" --no-build-isolation

COPY . .

CMD [ "uv", "run", "python", "-m", "src.app"]
