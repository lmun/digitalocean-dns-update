import requests
from datetime import datetime
from ipaddress import ip_address
from os import path
from configfile import config

file_path = path.dirname(path.abspath(__file__))

TOKEN = config.get('token')
DOMAIN = config.get('domain', 'example.com')
RECORD_ID = config.get('record_id')
LOG_LOCATION = path.join(file_path, 'log.txt')

print(LOG_LOCATION)

def main():
    with open(LOG_LOCATION, 'a') as f:
        try:
            actual_ip = str(ip_address(
                requests.get('https://api.ipify.org').text))
            record = requests.get(f'https://api.digitalocean.com/v2/domains/{DOMAIN}/records/{RECORD_ID}', headers={
                'Authorization': f'Bearer {TOKEN}'}).json()
            registered_ip = str(ip_address(record['domain_record']['data']))
            if actual_ip != registered_ip:
                f.write(
                    f'{datetime.now().isoformat()} - Actual IP: {actual_ip} - Registered IP: {registered_ip}\n')
                r = requests.patch(f'https://api.digitalocean.com/v2/domains/{DOMAIN}/records/{RECORD_ID}', headers={
                    'Authorization': f'Bearer {TOKEN}'}, json={
                        'data': actual_ip,
                        'type': 'A',
                        'ttl': 1200
                })
                if r.status_code != 200:
                    raise Exception(r.text)
                else:
                    print(r.text)
                    f.write(
                        f'{datetime.now().isoformat()}\tupdated {actual_ip} {registered_ip}\n')
        except Exception as e:
            isonow = datetime.now().isoformat()
            f.write(f'{isonow}\t{e}\n')


if __name__ == '__main__':
    main()
