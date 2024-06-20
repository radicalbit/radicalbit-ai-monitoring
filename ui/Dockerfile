FROM node:20.10.0-bullseye AS build

WORKDIR /app

COPY . .

RUN npm install --global --force yarn@1.22.21 && \
    yarn install && \
    yarn build:dev

FROM nginx:alpine3.19

EXPOSE 80

COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf