# syntax=docker/dockerfile:1
FROM python:latest

# install app
WORKDIR /src

COPY . .

# final configuration

RUN pip install requests

CMD ["python", "/src/ main.py"]

EXPOSE 3000
