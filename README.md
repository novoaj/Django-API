Dockerized Django API for my recipe app

build docker image:
```bash
docker build -t api .
```

run docker container on port 8000 with port forwarding:
```bash
docker run -p 8000:8000 api
```

