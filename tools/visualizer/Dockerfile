FROM node:alpine as build

WORKDIR /usr/local/src/visualizer/
RUN apk --no-cache add openjdk11 && \
        npm -g install shadow-cljs
COPY shadow-cljs.edn .
COPY public public
COPY src src
RUN shadow-cljs release visualizer


FROM nginx:alpine

COPY --from=build /usr/local/src/visualizer/public /usr/share/nginx/html/
