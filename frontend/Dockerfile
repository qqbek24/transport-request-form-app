FROM node:18-alpine

WORKDIR /app

# Proxy settings for corporate network
ENV https_proxy='http://165.225.206.24:10299' \
    http_proxy='http://165.225.206.24:10299' \
    no_proxy='localhost,127.0.0.1,backend,frontend,nginx'

# Install CA certificates
RUN apk add --no-cache ca-certificates
COPY ./zscaler.crt /usr/local/share/ca-certificates/
RUN update-ca-certificates

# Set NODE_EXTRA_CA_CERTS so Node.js uses the updated CA bundle
ENV NODE_EXTRA_CA_CERTS=/etc/ssl/certs/ca-certificates.crt

# Disable strict SSL for npm (corporate environment)
RUN npm config set strict-ssl false

# Install dependencies
COPY ./frontend/package*.json ./
RUN npm install

# Copy frontend code
COPY ./frontend .

# Expose port 3000
EXPOSE 3000

# Start the development server with host binding
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "3000"]