FROM node:20.10.0-bullseye AS dev

WORKDIR /app

COPY . .

RUN npm install --global --force yarn@1.22.21 && \
    yarn install

FROM node:20.10.0-bullseye AS build

WORKDIR /app

COPY . .
COPY --from=dev /app/node_modules /app/node_modules

RUN yarn build:prod

FROM nginx:alpine3.19

EXPOSE 80

COPY --from=build /app/dist /usr/share/nginx/html/
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY env.sh /docker-entrypoint.d/
RUN chmod +x /docker-entrypoint.d/env.sh