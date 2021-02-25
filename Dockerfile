FROM python:3
MAINTAINER zhangolve@gmail.com

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# CMD [ "python", "./monthly.py" ]

# Add crontab file in the cron directory
ADD crontab /etc/cron.d/hello-cron

# # Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/hello-cron

# # Create the log file to be able to run tail
RUN touch /var/log/cron.log

# #Install Cron
RUN apt-get update
RUN apt-get -y install cron


# Run the command on container startup
CMD cron && tail -f /var/log/cron.log
