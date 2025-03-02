    # Stage 1: Build the Angular app
    FROM node:latest as builder
    WORKDIR /app
    COPY package*.json ./
    RUN npm install
    COPY . .
    RUN npm run build

    # Stage 2: Serve the app with Nginx
    FROM nginx:latest
    COPY --from=builder /app/dist/wordrix-client /usr/share/nginx/html
    EXPOSE 80
    CMD ["nginx", "-g", "daemon off;"]