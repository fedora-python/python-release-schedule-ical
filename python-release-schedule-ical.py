#!/bin/python3

import re
import requests
from ics import Calendar

calendar_filename = 'python-releases.ics'

def uid(name):
    user = re.sub(r'[^a-z0-9\.]+', '', name.lower())
    return f'{user}@python.org'


r = requests.get('https://peps.python.org/release-schedule.ics')
r.raise_for_status()

c = Calendar(r.text)

for event in c.events:
    event.description = 'DEPRECATED: Use https://peps.python.org/release-schedule.ics instead'
    event.uid = uid(event.name)

with open(calendar_filename, 'w') as write_file:
    write_file.write(c.serialize())
