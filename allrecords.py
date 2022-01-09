#!/usr/bin/env python3
import requests
import json
from configfile import config

TOKEN = config.get('token')
DOMAIN = config.get('domain', 'example.com')

def main():
    do = requests.get(f'https://api.digitalocean.com/v2/domains/{DOMAIN}/records', headers={
                      'Authorization': f'Bearer {TOKEN}'}).json()
    for domain in do['domain_records']:
        print(domain)


if __name__ == '__main__':
    main()
