#!/bin/python3

import requests
from bs4 import BeautifulSoup
from ics import Calendar, Event
import dateutil.parser
import datetime

python_version_pep = {
    '3.5': 'pep-0478',
    '3.6': 'pep-0494',
    '3.7': 'pep-0537',
    '3.8': 'pep-0569',
    '3.9': 'pep-0596',
}

pep_url = 'https://www.python.org/dev/peps/'

c = Calendar()

for version, pep in python_version_pep.items():
    r = requests.get(pep_url + pep)
    soup = BeautifulSoup(r.text, 'lxml')
    for item in soup.find("div", {"id": "release-schedule"}).find_all("li"):
        e = Event()
        try:
            e.name = item.text.split(':')[0]
            start_date = dateutil.parser.parse(item.text.split(':')[1])
            e.begin = start_date
            e.end = start_date + datetime.timedelta(days=1)
            c.events.add(e)
        except:
            pass

with open('python-releases.ics', 'w') as my_file:
    my_file.writelines(c)
