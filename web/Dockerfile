# syntax=docker/dockerfile:1
FROM python:3.10-alpine
WORKDIR /web
ENV FLASK_APP=web.py
ENV FLASK_RUN_HOST=0.0.0.0
RUN apk add --no-cache gcc musl-dev linux-headers
COPY req.txt .
RUN pip install -r req.txt
EXPOSE 80
COPY . .
CMD ["flask", "run", "--debug"]