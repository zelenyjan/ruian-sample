FROM node:16-alpine

WORKDIR /app
COPY package.json /
COPY package-lock.json /

RUN npm install -g npm
RUN npm i -g webpack && npm i -g webpack-cli && npm i
CMD rm -rf node_modules && npm run serve
