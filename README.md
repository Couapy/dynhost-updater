# DynHostUpdater

Allow you to update your dynhost domains with CRON

## Installation

Please run the following command to get all dependencies :

> pip install -r requirements.txt

## Configuration

Create a *sites.conf*

And write the folling lines to add a domain :

```ini
[mysite.com]
user=mysuser
password=mypassword
```

If you want to add a new domain to update, you can paste a new section.

## Install CRON service

> sudo touch /var/log/DynDNSUpdate.log

`*/15 *  * * *   root    /bin/python3 /path/to/your/update.py >> /var/log/DynDNSUpdate.log`
