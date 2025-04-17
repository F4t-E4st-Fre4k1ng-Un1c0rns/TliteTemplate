FROM ghcr.io/astral-sh/uv:python3.10-alpine

WORKDIR /t-lite

COPY pyproject.toml uv.lock .
RUN uv sync --frozen

COPY . .
CMD [ "python", "--version"]
