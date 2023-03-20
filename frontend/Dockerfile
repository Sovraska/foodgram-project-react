# build env
FROM node:13.12.0-alpine as build
WORKDIR /app
COPY package*.json ./
RUN npm install --silent
RUN npm install react-scripts@1.1.1 -g --silent
COPY . ./
RUN npm run build
CMD cp -r build result_build
CMD ["yarn", "start"]