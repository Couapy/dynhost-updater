"""
Dynhost updater
"""
import json
import socket
import requests
import configparser

class Domain:
    """Domain object"""

    def __init__(self, domain, user, password):
        self.domain = domain
        self.auth = (user, password)
        self.device_ip = ''
        self.server_ip = ''

    def update(self, device_ip):
        """Update the dynhost of the domain"""
        self.device_ip = device_ip
        error = False
        try:
            req = resquests.get(URL_UPDATE_IP)
            self.server_ip = req.text
        except Exception as e:
            error = True

        if error:
            print('[ERROR]Impossible de récupérer l\'adresse ip du serveur')
        elif self.server_ip != self.device_ip:
            print()
            print('[WARN]Le domaine "{}" n\'est pas à jour'.format(self.domain))
            self.update_dynhost(device_ip)
        else:
            print('[INFO]Le domaine "{}" est à jour'.format(self.domain))

    def update_dynhost(self, device_ip):
        """Update online the DNS"""
        print('[INFO]IP actuelle : {}'.format(self.server_ip))
        print('[INFO]IP nouvelle : {}'.format(self.device_ip))
        print('[INFO]Mise à jour en cours...')
        req = requests.get(URL_UPDATE.format(
            self.domain, device_ip), auth=self.auth)
        if req.status_code == 200:
            print('[SUCCESS]Mise à jour réussie')
        elif req.status_code == 401:
            print('[ERROR]Identification incorrecte')
        else:
            print('[ERROR]Erreur inconnue')


# CONFIG
URL_UPDATE = 'http://www.ovh.com/nic/update?system=dyndns&hostname={}&myip={}'
URL_UPDATE_IP = 'https://ifconfig.me/ip'

# Config parser
config = configparser.ConfigParser()
config.read('sites.conf')

# App
domains = []
device_ip = ''

# Update device ip
req = requests.get('http://ifconfig.co/json')
response = json.loads(req.text)
device_ip = response['ip']

for domain in config.sections():
    domains.append(Domain(domain, config[domain]['user'], config[domain]['password']))

print("[INFO]Application starting", end="\n")
for domain in domains:
    domain.update(device_ip)
