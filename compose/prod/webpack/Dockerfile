FROM node:16-alpine

WORKDIR /app

# copy project
COPY . .

RUN npm install
RUN npm run gettext:compile && \
    npm run build:prod && \
    npm run build:admin:prod && \
    npm run build:dev && \
    npm run build:admin:dev
