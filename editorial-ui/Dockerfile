FROM node:16

ARG API_BASE_URL
ENV REACT_APP_API_BASE_URL=$API_BASE_URL

WORKDIR /app
COPY . .

RUN yarn install
RUN REACT_APP_API_BASE_URL=$API_BASE_URL yarn build

FROM nginx:1.21

COPY --from=0 /app/build/ /usr/share/nginx/html
