#!/usr/bin/env python

import asyncore
import socket
from asyncore import dispatcher_with_send as DWS
from collections import namedtuple
HostPort = namedtuple('HostPort', ['host', 'port'])

class ConnectionInitiator(DWS):
    def __init__(self, connection):
        DWS.__init__(self)
        self.connection = connection
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect(connection.server.connectTo)

    def handle_connect(self):
        print "Handle connect"

    def handle_close(self):
        print "handle close"
        self.connection.receiver.close()
        self.close()

    def handle_read(self):
        print "Handle read"
        x = self.recv(8192)
        sent = self.connection.receiver.send(x)
        print "Sent %s of %s" % (len(x), sent)

class ConnectionReceiver(DWS):
    def __init__(self, connection, sock):
        DWS.__init__(self, sock)
        self.connection = connection

    def handle_read(self):
        print "Handle read"
        x = self.recv(8192)
        print vars(self.parent.initiator)
        self.connection.initiator.send(x)

    def handle_connect(self):
        print "Handle connect"

    def handle_close(self):
        print "handle close"
        self.connection.initiator.close()
        self.close()

class ProxyConnection:
    def __init__(self, server, sock):
        self.server = server
        self.sock = sock
        print "Create initiator"
        self.initiator = ConnectionInitiator(self)
        print "Create receiver"
        self.receiver = ConnectionReceiver(self, sock)

class ProxyServer(asyncore.dispatcher):
    def __init__(self,
                 listenOn,
                 connectTo):
        asyncore.dispatcher.__init__(self)
        self.listenOn  = listenOn
        self.connectTo = connectTo
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        
        self.set_reuse_addr()
        self.bind(listenOn)
        self.listen(5)

    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            print 'Incoming connection from %s' % repr(addr)
            ProxyConnection(self, sock)

server = ProxyServer(
    HostPort('localhost', 8090),
    HostPort('localhost', 8080))

asyncore.loop()

