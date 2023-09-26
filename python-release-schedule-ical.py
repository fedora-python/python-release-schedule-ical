#!/bin/python3

import re
import requests
import sys
from bs4 import BeautifulSoup
from ics import Calendar, Event
import dateutil.parser

python_version_pep = {
    '3.5': 'pep-0478',
    '3.6': 'pep-0494',
    '3.7': 'pep-0537',
    '3.8': 'pep-0569',
    '3.9': 'pep-0596',
    '3.10': 'pep-0619',
    '3.11': 'pep-0664',
    '3.12': 'pep-0693',
    '3.13': 'pep-0719',
}

pep_url = 'https://www.python.org/dev/peps/'
calendar_filename = 'python-releases.ics'

def uid(name):
    user = re.sub(r'[^a-z0-9\.]+', '', name.lower())
    return f'{user}@python.org'


c = Calendar()

for version, pep in python_version_pep.items():
    url = pep_url + pep
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    for item in soup.find("section", {"id": "release-schedule"}).find_all("li"):
        try:
            name, start_date = item.text.splitlines()[0].split(':')
            if ' (' in start_date:  # 2020-08-14 (expected)
                start_date, _, note = start_date.partition(' (')
                name = f'{name} ({note}'
            if not name.startswith('Python '):
                name = f'Python {name}'
            e = Event(name=name, uid=uid(name), url=url)
            e.begin = dateutil.parser.parse(start_date)
            e.make_all_day()
            c.events.add(e)
        except Exception:
            print(f'Warning: Cannot parse {item.text!r}', file=sys.stderr)

with open(calendar_filename, 'w') as write_file:
    for line in c:
        write_file.write(line)
        if 'PRODID' in line:
            write_file.write("X-WR-CALNAME:Python releases schedule\n")
            write_file.write("X-WR-CALDESC:Python releases schedule parsed from https://www.python.org/dev/peps/\n")

