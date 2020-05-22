"""
Dynhost updater
"""
import json
import socket
from configparser import ConfigParser
from datetime import datetime

import requests


class Domain:
    """Domain object"""

    def __init__(self, domain, user, password):
        self.domain = domain
        self.auth = (user, password)
        self.device_ip = ''

    def update(self, device_ip):
        """Update online the DNS"""
        print('[DOMAIN] ' + self.domain)
        print('[INFO] IP : {}'.format(device_ip))
        req = requests.get(URL_UPDATE.format(
            self.domain, device_ip), auth=self.auth)
        if req.status_code == 200:
            print('[SUCCESS] IP update successfull')
        elif req.status_code == 401:
            print('[ERROR] Wrong credentials')
        else:
            print('[ERROR] Unexpected error')


# CONFIG
URL_UPDATE = 'http://www.ovh.com/nic/update?system=dyndns&hostname={}&myip={}'
URL_UPDATE_IP = 'https://ifconfig.me/ip'

# Config parser
config = ConfigParser()
config.read('sites.conf')

# App
domains = []
device_ip = ''

# Update device ip
req = requests.get(URL_UPDATE_IP)
device_ip = req.text

for domain in config.sections():
    domains.append(Domain(domain, config[domain]['user'], config[domain]['password']))

print('[DATE] ' + str(datetime.now()))
for domain in domains:
    domain.update(device_ip)
