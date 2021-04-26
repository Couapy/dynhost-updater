FROM python:3.9

# Install CRON
RUN apt-get -qq update && apt-get install -yqq cron
COPY config/cron.conf /etc/cron.d/dynhostupdater
RUN chmod +x /etc/cron.d/dynhostupdater
RUN crontab /etc/cron.d/dynhostupdater

# Install application
WORKDIR /app
COPY requirements.txt .
RUN pip -q install -r requirements.txt
COPY . .
