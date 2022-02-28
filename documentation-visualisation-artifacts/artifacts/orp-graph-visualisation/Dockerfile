FROM node:16

WORKDIR /app
COPY . .

RUN npm ci
RUN npm run build

FROM nginx:1.21

COPY --from=0 /app/ /usr/share/nginx/html/graph_visualisation