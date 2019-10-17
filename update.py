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
            self.update_dynhost()
            self.notification()

    def update_dynhost(self):
        """Update online the DNS"""
        # TEMP: is temp
        device_ip = '90.22.66.151'
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

    def notification(self):
        """Send an email to me to notifiate that the domain had changed IP"""
        print('[INFO]Envoie du mail de notification en cours...')
        import smtplib

        try:
            subject = 'Notification system : DNS updated !'
            toaddrs = [TO]
            message = """
Le domaine {} a changé d'adresse !
Ancienne adresse : {}
Nouvelle adresse : {}
            """.format(self.domain, self.server_ip, self.device_ip)
            msg = """\
From: %s\r\n\
To: %s\r\n\
Subject: %s\r\n\
\r\n\
%s
            """ % (FROM, ", ".join(toaddrs), subject, message)

            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()
            server.login(FROM, PASSWORD)
            server.sendmail(FROM, TO, msg.encode())
            server.quit()
        except smtplib.SMTPAuthenticationError as error:
            print("[ERROR]Bad authentification : " + str(error))
        except Exception as error:
            print('[ERROR]Unknow : ' + str(error))
        else:
            print("[SUCCESS]Le mail a bien été envoyé !")


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
FROM = "jean.dupont@exemple.fr"
PASSWORD = "password"
SMTP_SERVER = "smtp.exemple.fr"
SMTP_PORT = 587
TO = "you@exemple.fr"

App()
