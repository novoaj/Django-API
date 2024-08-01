# Dockerized Django API for my recipe app
frontend repository can be found here: https://github.com/novoaj/MobileRecipe 

This project is a Dockerized Django API with JWT authentication for a mobile recipe app. The app's dependencies are specified in requirements.txt which rely on Python3.11. This app uses Django Rest Framework, which simplifies building APIs. This API was developed on an AWS ec2 instance using Amazon Linux 2023. This API interacts with a PostgreSQL database hosted on AWS. 

## Technologies used:
- Python3.11
- Django
- Django Rest Framework
- PostgreSQL
- AWS Elastic Compute Cloud (EC2)
- AWS Relation Database Services (RDS)

## Get started
### Prerequisites
- Docker installed on your machine
- Python3.11

### Docker Instructions

1. Navigate to directory containing docker file using cd and ls commands.
2. Use docker build command:
```bash
docker build -t <imagename> .
```
3. See your new docker image:
```bash
docker images
```
4. Run docker container on port 8000 with port forwarding. (optional) Add -d flag to run container in background:
```bash
docker run -p 8000:8000 <imagename>
docker run -d -p 8000:8000 <imagename>
```
5. Find name/id of docker container
```bash
docker ps -a
```
6. Kill the running container. If container is not running, proceed to next step
```bash
docker kill <imagename/id>
```
7. Remove the container:
```bash
docker rm <imagename/id>
```


