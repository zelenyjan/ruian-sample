FROM node:16-alpine

WORKDIR /app

# copy project
COPY . .

RUN npm install
RUN npm run build:prod && \
    npm run build:dev
