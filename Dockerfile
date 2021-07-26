# syntax=docker/dockerfile:1
FROM python:3.9-slim-buster
WORKDIR /
ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0
RUN apk add --no-cache gcc musl-dev linux-headers
COPY req.txt req.txt
RUN pip install -r req.txt
EXPOSE 5000
COPY . .
CMD ["flask", "run"]