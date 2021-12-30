FROM node:12-alpine
# adding build tools to make yarn install work on Apple silicon/arm64 machine
RUN apk add --no-cache python2 g++ make
WORKDIR /app
COPY package.json yarn.lock ./
RUN yarn install --production
COPY . .
CMD ["node", "src/index.js"]
