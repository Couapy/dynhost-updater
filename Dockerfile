FROM python:3.9

# Configure locale (log date & time)
ENV TZ=Europe/Paris
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Install application
WORKDIR /app
COPY requirements.txt .
RUN pip -q install -r requirements.txt
COPY . .
