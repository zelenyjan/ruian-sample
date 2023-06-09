FROM python:3.10-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONMALLOC debug
ENV PYTHONFAULTHANDLER 1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends gcc python3-dev netcat libcairo2-dev pkg-config libjpeg-dev zlib1g-dev

RUN pip install poetry
COPY poetry.lock pyproject.toml ./
RUN POETRY_VIRTUALENVS_CREATE=false poetry install --no-root

ENTRYPOINT ["./compose/local/app/entrypoint"]
