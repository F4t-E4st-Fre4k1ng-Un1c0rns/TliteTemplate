FROM nvidia/cuda:12.6.1-runtime-ubuntu20.04
WORKDIR /t-lite

RUN curl -LsSf https://astral.sh/uv/install.sh | sh

COPY pyproject.toml uv.lock .
RUN uv python install
RUN uv sync --frozen

COPY . .
CMD [ "uv", "run", "python", "-m", "src.app"]
