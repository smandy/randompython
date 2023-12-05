import asyncio
import logging
import socket
import asyncore
import sys

docs = []


class expose:
    def __init__(self, doc):
        self.doc = doc

    def __call__(self, fn):
        docs.append((fn.__name__, self.doc))
        return fn


class CommandHandler(asyncio.async_chat):
    # ac_in_buffer_size = 64
    # ac_out_buffer_size = 64
    def __init__(self, sock):
        self.received_data = []
        self.logger = logging.getLogger('CommandHandler')
        asyncio.async_chat.__init__(self, sock)
        # Start looking for the ECHO command
        self.set_terminator('\n')
        self.prompt()
        self.docstring = "\n%s\n" % "\n".join([f"{q:20} : {v:20}"
                                               for q, v in docs])
        self.commandSet = {x[0] for x in docs}
        print(self.commandSet)

    @expose('Get some help')
    def help(self):
        self.send(self.docstring)

    @expose('Flip all orders')
    def flip(self, args):
        print(f"Flip all orders {args}")

    def prompt(self):
        self.send("eurem >>> ")

    def collect_incoming_data(self, data):
        """Read an incoming message from the client
        and put it into our outgoing queue."""
        self.logger.debug('collect_incoming_data() -> (%d bytes)\n"""%s"""',
                          len(data), data)
        self.received_data.append(data)

    def found_terminator(self):
        self.logger.debug('found_terminator()')
        # TODO - split on return - stick remain in buffer.
        print(self.received_data)
        args = [x.strip() for x in self.received_data[0].strip().split()]

        print(f"Args {args}")
        if args:
            cmd, rest = args[0], args[1:]
            if cmd in self.commandSet:
                # newArgs = [self] + rest
                # print "Newargs are %s" % str(newArgs)
                getattr(self, cmd)(*rest)
            else:
                self.send(f"{cmd} ??? \n\n{self.docstring}\n")
        self.received_data = []
        self.prompt()

    def process_data(self, *args):
        print(f"Process data {args}")


class CommandServer(asyncore.dispatcher):
    """Receives connections and establishes handlers for each client.
    """

    def __init__(self, addr):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind(addr)
        self.address = self.socket.getsockname()
        self.listen(1)

    def handle_accept(self):
        # Called when a client connects to our socket
        client_info = self.accept()
        CommandHandler(sock=client_info[0])

    def handle_close(self):
        self.close()


print(docs)

logging.basicConfig(level=logging.DEBUG,
                    format='%(name)s: %(message)s',
                    )

port = int(sys.argv[1])
print(port)

address = ('localhost', port)  # let the kernel give us a port
server = CommandServer(address)
ip, port = server.address  # find out what port we were given
asyncore.loop()
