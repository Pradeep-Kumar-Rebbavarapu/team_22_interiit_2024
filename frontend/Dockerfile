# Node version
FROM node:20

WORKDIR /app

COPY package*.json ./
RUN npm install --force

COPY . .

EXPOSE 3000

RUN npm run build

RUN npm run start
