# Dockerized Django API for my recipe app
This project is a Dockerized Django API for a recipe app. The app's dependencies are specified in requirements.txt, and it relies on Python3.11.
This app uses Django Rest Framework, which simplifies building APIs. This API was developed on an AWS ec2 instance using Amazon Linux 2023.

## Prerequisites
- Docker installed on your machine
- Python3.11

## Docker instructions

build docker image:
```bash
docker build -t api .
```

run docker container on port 8000 with port forwarding. Add -d flag to run container in background:
```bash
docker run -p 8000:8000 api
docker run -d -p 8000:8000 api

