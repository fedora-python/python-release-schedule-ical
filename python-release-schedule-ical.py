#!/bin/python3

import re
import requests
from bs4 import BeautifulSoup
from ics import Calendar, Event
import dateutil.parser

python_version_pep = {
    '3.5': 'pep-0478',
    '3.6': 'pep-0494',
    '3.7': 'pep-0537',
    '3.8': 'pep-0569',
    '3.9': 'pep-0596',
}

pep_url = 'https://www.python.org/dev/peps/'


def uid(name):
    user = re.sub(r'[^a-z0-9\.]+', '', name.lower())
    return f'{user}@python.org'


c = Calendar()


for version, pep in python_version_pep.items():
    r = requests.get(pep_url + pep)
    soup = BeautifulSoup(r.text, 'lxml')
    for item in soup.find("div", {"id": "release-schedule"}).find_all("li"):
        try:
            name, start_date = item.text.split(':')
            if not name.startswith('Python '):
                name = f'Python {name}'
            e = Event(name=name, uid=uid(name))
            e.begin = dateutil.parser.parse(start_date)
            e.make_all_day()
            c.events.add(e)
        except Exception:
            pass

with open('python-releases.ics', 'w') as my_file:
    my_file.writelines(c)
