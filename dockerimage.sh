#!/bin/sh

# Сборка Docker-образа
docker build -t sergiokapone/fastapi11 .

docker push sergiokapone/fastapi11

# Запуск контейнера с монтированием volumes
docker run -p 8000:8000 -it sergiokapone/fastapi11
