#!/usr/bin/python
#
#    Copyright (C) 2013 Loic Dachary <loic@dachary.org>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# python dns_spoof.py 8.8.8.8
#
import sys
from twisted.internet import reactor
from twisted.names import dns
from twisted.names import client, server

class DNSSpoofFactory(server.DNSServerFactory):

    def __init__(self, fqdn2fqdn, authorities = None, caches = None, clients = None, verbose = 0):
        self.fqdn2fqdn = fqdn2fqdn
        args = (self, authorities, caches, clients, verbose)
        server.DNSServerFactory.__init__(*args)

    def handleQuery(self, message, protocol, address):
        query = message.queries[0]
        if query.name.name in self.fqdn2fqdn:
            spoofed = query.name.name
            query.name.name = self.fqdn2fqdn[query.name.name]
        else:
            spoofed = False

        return self.resolver.query(query).addCallback(
            self.gotResolverResponse, spoofed, protocol, message, address
            ).addErrback(
            self.gotResolverError, spoofed, protocol, message, address
            )

    def gotResolverResponse(self, (ans, auth, add), spoofed, protocol, message, address):
        if spoofed:
            message.queries[0].name.name = spoofed
            ans[0].name.name = spoofed
        args = (self, (ans, auth, add), protocol, message, address)
        return server.DNSServerFactory.gotResolverResponse(*args)

    def gotResolverError(self, failure, spoofed, protocol, message, address):
        if spoofed:
            message.queries[0].name.name = spoofed
        args = (self, failure, protocol, message, address)
        return server.DNSServerFactory.gotResolverError(*args)

if __name__ == '__main__':
    from spoof_map import fqdn2fqdn

    verbosity = 0
    resolver = client.Resolver(servers=[(sys.argv[1], 53)])
    factory = DNSSpoofFactory(fqdn2fqdn, clients=[resolver], verbose=verbosity)
    protocol = dns.DNSDatagramProtocol(factory)
    factory.noisy = protocol.noisy = verbosity
    reactor.listenUDP(53, protocol)
    reactor.listenTCP(53, factory)
    reactor.run()
