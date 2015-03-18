#!/usr/bin/env python
#
# Restart all Deis apps by scaling all processes to zero and then back
# to their original number.
#
# Run after a Deis backup restore to refresh Deis status
import subprocess
import time

import deis

cli = deis.DeisClient()
response = cli._dispatch('get', '/v1/apps')

for app in response.json()['results']:
    for runner, count in app['structure'].items():
        if runner == 'run':
            continue
        subprocess.call(['deis', 'scale', '{}=0'.format(runner), '-a', app['id']])
        # Give some breathing time to Deis or it returns 503 Service Unavailable.
        time.sleep(5)
        subprocess.call(['deis', 'scale', '{}={}'.format(runner, count), '-a', app['id']])
