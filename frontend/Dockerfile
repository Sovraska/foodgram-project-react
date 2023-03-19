# build env
FROM node:18.0.0 as build
WORKDIR /app
COPY package*.json ./
RUN yarn install
COPY . ./
RUN yarn run build
CMD cp -r build result_build
CMD ["yarn", "start", "build"]