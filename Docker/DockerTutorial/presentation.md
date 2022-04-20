# 1
#### Why Docker?

- Fast and easy to save, share, and deploy working code environments
- Allows for deployment on any OS

# 2
#### Installation

- Install from docs.docker.com/get-docker/
- Create an account on hub.docker.com
- Make sure Docker is running in your environment (whale icon in toolbar)

# 3
#### Images and Containers

- docker pull alpine:latest
- docker run -it alpine:latest
- docker run python:latest
- docker run python:3.10-alpine
- docker run -it python:latest bash
- docker container ls -a

# 5
#### DockerHub

- See Python versions

# 6
#### Hello World Example

- Dockerfile
- docker build -t hello-world .
- docker tag -t hello-world bucketoffish/hello-world
- docker push bucketoffish/hello-world

# 7
#### REDFOR Example

- Dockerfile
- Order of layers

# 8
#### Docker Compose

- REDFOR example
