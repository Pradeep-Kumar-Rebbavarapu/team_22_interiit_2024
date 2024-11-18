# Node version
FROM node:20

WORKDIR /app

COPY package*.json ./
RUN npm install --force

COPY . .

EXPOSE 3033

COPY entrypoint.sh /
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/bin/sh", "/entrypoint.sh"]
