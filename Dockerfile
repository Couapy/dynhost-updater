FROM python:3.9

# Install CRON
RUN apt update && apt install -yqq cron
COPY hello-cron /etc/cron.d/dynhostupdater
RUN chmod 0644 /etc/cron.d/dynhostupdater
RUN crontab /etc/cron.d/dynhostupdater

# Install application
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

# Create default logs
RUN mkdir -p logs
RUN touch logs/lastest.log
