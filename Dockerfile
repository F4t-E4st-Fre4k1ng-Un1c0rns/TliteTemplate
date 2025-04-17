FROM ghcr.io/astral-sh/uv:python3.10-bookworm

WORKDIR /t-lite

COPY pyproject.toml uv.lock .
RUN uv sync --frozen

COPY . .
CMD [ "uv", "run", "src/app.py"]
