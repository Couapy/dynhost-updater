import logging
import os
import sys
from configparser import ConfigParser

import dns.resolver
import requests

SITES_CONFIG = 'config/sites.cfg'
URI_UPDATE = 'http://www.ovh.com/nic/update?system=dyndns&hostname=%(hostname)s&myip=%(ip)s'
URI_GET_IP = 'https://ifconfig.me/ip'
DNS_RESOLVERS = ['8.8.8.8']


class Domain:
    """Represent a domain or sub-domain that can update DNS entries with DynHost (ovh)."""

    def __init__(self, domain: str, user: str, password: str):
        """Instanciate the domain object."""
        self.domain = domain
        self.credentials = (user, password)
        self.logger = logging.getLogger(self.domain)
        self.old_ip = None

    def is_update_to_date(self, current_ip) -> bool:
        """Indicates if the domain address is up to date."""
        my_resolver = dns.resolver.Resolver()
        my_resolver.nameservers = DNS_RESOLVERS
        answers = my_resolver.resolve(
            qname=self.domain,
            rdtype='A',
        )
        self.old_ip = answers[0].address
        return answers[0].address == current_ip

    def update(self, current_ip: str) -> None:
        """Update DNS entry only if the DNS address ip is outdated."""
        if self.is_update_to_date(current_ip):
            return

        data = {
            'hostname': self.domain,
            'ip': current_ip,
        }
        req = requests.get(
            url=URI_UPDATE % data,
            auth=self.credentials,
        )
        if req.status_code == 200:
            self.logger.info('Successfully updated from %s to %s.' %
                             (self.old_ip, current_ip))
        elif req.status_code == 401:
            self.logger.error('Failed to update DNS. Bad credentials.')
        else:
            self.logger.error(
                'Failed to update DNS. Unexpected error happened.')


def get_current_ip() -> str:
    """Returns the current device ip address."""
    req = requests.get(URI_GET_IP)
    return req.text


def main():
    """Configure logs, and update the domains configured in SITES_CONFIG file."""
    os.makedirs('logs', exist_ok=True)
    logging.basicConfig(
        format='[%(asctime)s][%(levelname)s][%(name)s] %(message)s',
        datefmt='%m/%d/%Y %H:%M:%S',
        level=logging.INFO,
        handlers=[
            logging.FileHandler('logs/lastest.log'),
            logging.StreamHandler()
        ],
    )
    if not os.path.exists(SITES_CONFIG):
        logging.error('sites.conf does not exists.')
        sys.exit(1)
    config = ConfigParser()
    config.read(os.path.join(SITES_CONFIG))

    current_ip = get_current_ip()

    for section in config.sections():
        domain = Domain(
            domain=section,
            user=config.get(section, 'user'),
            password=config.get(section, 'password'),
        )
        domain.update(current_ip)


if __name__ == '__main__':
    main()
