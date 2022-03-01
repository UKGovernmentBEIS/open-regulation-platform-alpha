FROM node:16

WORKDIR /app
COPY . .

RUN npm ci

RUN npm run build
RUN npm run generate

FROM nginx:1.21

COPY --from=0 /app/dist/ /usr/share/nginx/html/api_documentation