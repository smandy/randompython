# Andy Smith <2018-01-23 Tue> Got it from here.
# https://gitlab.kitware.com/third-party/twisted/raw/f5e0d4b7cd3c2a838a5916d14ca629d5ac4549ee/doc/examples/qtdemo.py
# WIll commit to git it'll need some hacks for qt5

# Twisted, the Framework of Your Internet
# Copyright (C) 2001 Matthew W. Lefkowitz
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of version 2.1 of the GNU Lesser General Public
# License as published by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

"""Qt demo.

Fetch a URL's contents.
"""

#import sys
#from PyQt5.QtWidgets import QApplication, QPushButton, QHBoxLayout, QGroupBox, QDialog, QVBoxLayout, QGridLayout, QLineEdit

from PyQt5.QtWidgets import QApplication, QVBoxLayout, QLabel, QLineEdit, QWidget, QHBoxLayout
import qt5reactor
import urllib
from twisted.internet import protocol
app = QApplication([])
qt5reactor.install()
from twisted.web import http

class TwistzillaClient(http.HTTPClient):
    def __init__(self, edit, urls):
        self.urls  = urls
        self.edit  = edit

    def connectionMade(self):
        print( 'Connected.')
        self.sendCommand('GET', self.urls[2])
        self.sendHeader('Host', '%s:%d' % (self.urls[0], self.urls[1]) )
        self.sendHeader('User-Agent', 'Twistzilla')
        self.endHeaders()

    def handleResponse(self, data):
        print( 'Got response.')
        self.edit.setText(data)

class TwistzillaWindow(QWidget):
    def __init__(self, *args):
        super().__init__()

        #self.setCaption("Twistzilla")

        hbox = QHBoxLayout()
        #vbox.setSpacing(3)
        self.label = QLabel("Address: ")
        hbox.addWidget(self.label)

        self.line  = QLineEdit("http://www.twistedmatrix.com/")
        hbox.addWidget(self.line)
        #self.connect(self.line, SIGNAL('returnPressed()'), self.fetchURL)
        self.edit = QLineEdit()
        #self.edit.setEditeda(0)
        hbox.addWidget(self.edit)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)

        self.setLayout(vbox)
        self.setWindowTitle("Woot")
        self.show()

    def fetchURL(self):
        u = urllib.parse.urlparse(str(self.line.text()))

        pos = u[1].find(':')

        if pos == -1:
            host, port = u[1], 80
        else:
            host, port = u[1][:pos], int(u[1][pos+1:])

        if u[2] == '':
            file = '/'
        else:
            file = u[2]

        print( 'Connecting to.')
        from twisted.internet import reactor
        protocol.ClientCreator(reactor, TwistzillaClient, self.edit, (host, port, file)).connectTCP(host, port)


def main():
    """Run application."""
    # hook up Qt application to Twisted
    from twisted.internet import reactor
    
    win = TwistzillaWindow()
    win.show()

    # make sure stopping twisted event also shuts down QT
    reactor.addSystemEventTrigger('after', 'shutdown', app.quit )

    # shutdown twisted when window is closed
    #app.connect(app, SIGNAL("lastWindowClosed()"), reactor.stop)

    reactor.run()


if __name__ == '__main__' or True:
    main()
