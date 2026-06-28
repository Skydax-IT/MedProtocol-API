FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY requirements.txt requirements-dev.txt ./
RUN uv pip install --system -r requirements-dev.txt

COPY app ./app
COPY migrations ./migrations
COPY tests ./tests
COPY docs ./docs
COPY examples ./examples
COPY alembic.ini pyproject.toml README.md ./

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
