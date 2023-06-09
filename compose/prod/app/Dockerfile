# pyhon builder
FROM python:3.10-slim-buster as builder

WORKDIR /usr/src/app

# install dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev libjpeg-dev libcairo2-dev pkg-config zlib1g-dev && \
    pip install --upgrade pip && \
    rm -rf /var/lib/apt/lists/*

# get requirements.txt from poetry file
RUN pip install --upgrade pip
RUN pip install poetry

COPY poetry.lock pyproject.toml ./

# convert poetry to requirements txt
RUN poetry export -f requirements.txt --dev --output requirements.txt
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt


# final python image
FROM python:3.10-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y --no-install-recommends netcat && \
    rm -rf /var/lib/apt/lists/*

# create the appropriate directories
ENV APP_NAME=ruian-sample
ENV APP_HOME=/var/www/$APP_NAME
RUN mkdir -p $APP_HOME

WORKDIR $APP_HOME

# copy wheels from builder
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --no-cache /wheels/*

# copy project
COPY . $APP_HOME

ENTRYPOINT ["./compose/prod/app/entrypoint"]
