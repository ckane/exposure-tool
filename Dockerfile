FROM node:23-alpine

# Install Python and nginx
RUN apk add --no-cache python3 py3-pip nginx

# Install Python dependencies
RUN apk add --no-cache py3-gunicorn py3-flask

# Change Workdir
RUN mkdir -p -m 755 /app
WORKDIR /app

# Copy over the backend and frontend components
COPY exposure-back ./exposure-back
COPY exposure-front ./exposure-front
COPY bootstrap.sh .

# Build front-end project
WORKDIR /app/exposure-front
RUN npm i
RUN npx vite build

# Clean up the intermediate NPM workspace
RUN rm -rf node_modules

# Create folder for reports if one doesn't exist
RUN mkdir -p -m 755 /data/reports

# Create folder for nginx logs
RUN mkdir -p -m 755 /app/exposure-front/logs

EXPOSE 8000

# Return to /app for execution
WORKDIR /app
ENTRYPOINT ["./bootstrap.sh"]
