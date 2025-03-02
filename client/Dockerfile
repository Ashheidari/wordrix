# Use a lightweight Nginx image
FROM nginx:alpine

# Set the working directory inside the container
WORKDIR /usr/share/nginx/html

# Remove default Nginx static files
RUN rm -rf ./*

# Copy built AngularJS application from local machine to the container
COPY ./dist /usr/share/nginx/html

# Expose port 80 to be accessible outside the container
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
