FROM python:3.12-slim

WORKDIR /app

# Install uv for faster dependency management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Copy dependency files first for better Docker layer caching
COPY pyproject.toml uv.lock ./

# Install dependencies using uv
RUN uv sync --frozen --no-cache

# Copy application code
COPY . .

# Expose the port that the FastMCP server runs on
EXPOSE 9000

# Run the server
CMD ["uv", "run", "python", "server.py"]

