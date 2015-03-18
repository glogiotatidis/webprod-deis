#!/usr/bin/env python
#
# Returns Deis platform version
import deis

cli = deis.DeisClient()
response = cli._dispatch('get', '/v1/apps')
print(response.headers.get('x_deis_platform_version', 'Could not determine version'))
