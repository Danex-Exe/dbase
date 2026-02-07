FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml requirements-dev.txt requirements.txt ./
COPY dbase ./dbase
COPY docs ./docs
COPY LICENSE ./

RUN python -m pip install --upgrade pip && pip install -e .[dev]

CMD ["pytest", "-q"]
