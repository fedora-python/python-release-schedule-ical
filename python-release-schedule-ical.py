#!/bin/python3
# /// script
# dependencies = [
#     "ics>=0.7",
#     "requests>=2.22",
# ]
# ///

import re
import requests
from ics import Calendar

DEPRECATION = 'DEPRECATED: Use https://peps.python.org/release-schedule.ics instead'

calendar_filename = 'python-releases.ics'

def uid(name):
    user = re.sub(r'[^a-z0-9\.]+', '', name.lower())
    return f'{user}@python.org'


r = requests.get('https://peps.python.org/release-schedule.ics')
r.raise_for_status()

c = Calendar(r.text)

for event in c.events:
    event.uid = uid(event.name)
    event.description = DEPRECATION
    event.name = f'{event.name} (this calendar URL is deprecated)'

for extra in c.extra:
    if extra.name == 'X-WR-CALNAME':
        extra.value = f'DEPRECATED: {extra.value}'
    elif extra.name == 'X-WR-CALDESC':
        extra.value = DEPRECATION

with open(calendar_filename, 'w') as write_file:
    write_file.write(c.serialize())
