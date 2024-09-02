FROM python:3.10-alpine
LABEL maintainer="Marian <marianfsdev@gmail.com>"

LABEL build_date="2024-09-02"
RUN apk update && apk upgrade
RUN apk add --no-cache git make build-base linux-headers
WORKDIR /discord_bot
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "-u", "index.py"]
