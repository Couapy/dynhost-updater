# dynhost-updater

[![MIT License](https://img.shields.io/badge/license-MIT-yellow.svg)](https://github.com/5kyc0d3r/upnpy/blob/master/LICENSE)
[![MIT License](https://img.shields.io/badge/python-3-brightgreen)](https://github.com/Couapy/DynHostUpdater/)

This is a tool that allow you to update DynHost (ovh technology) fields automatically.

## How to execute ?

The recommanded way to execute this tool is docker.

### With Docker

This tool can be executed in a container with docker :

```bash
docker-compose up -d
```

### Locally

Please run the following command

```
pip install virtualenv
virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt

# To execute the script once:
python3 main.py
```

To execute automatically the script, you can use the `config/con.conf` cron file. 

## Configuration

The configuration is stored in the `config/sites.cfg` file.

For example, the script will update **mysite.com** with the user `myuser` and password `mypassword`:

```ini
[mysite.com]
user=mysuser
password=mypassword
```

If you want more domains, just create new sections.
