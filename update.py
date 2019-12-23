"""
Dynhost updater
"""
import json
import socket
import requests

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
        self.server_ip = socket.gethostbyname(self.domain)
        if self.server_ip != self.device_ip:
            print()
            print('[INFO]Le domaine "{}" n\'est pas à jour'.format(self.domain))
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

class App:
    """Classe principale de mon application"""

    def __init__(self):
        self.domains = []
        self.device_ip = ''
        self.update_current_ip()
        self.set_domains()
        self.run()

    def update_current_ip(self):
        """Update the current IP"""
        req = requests.get('http://ifconfig.co/json')
        response = json.loads(req.text)
        self.device_ip = response['ip']

    def set_domains(self):
        """Create array of domain objects"""
        # self.domains.append(Domain('domain', 'user', 'password'))

    def run(self):
        """Core application"""
        print("[INFO]Application starting", end="\n")
        for domain in self.domains:
            domain.update(self.device_ip)

#CONFIG
URL_UPDATE = 'http://www.ovh.com/nic/update?system=dyndns&hostname={}&myip={}'

App()
