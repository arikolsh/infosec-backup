import scapy.all as S
import subprocess


def format_packet(packet):
    """
    Return a pretty, readable, representation of the packet.
    """
    return repr(packet)


def packet_filter(packet):
    """
    A sample filter to match only PING requests.
    """
    return packet.haslayer(S.ICMP) and (
        # See https://en.wikipedia.org/wiki/Internet_Control_Message_Protocol
        packet[S.ICMP].type == 8 # echo-request
    )


def parse_packet(packet):
    return '%s is sending a ping to %s' % (packet[S.IP].src, packet[S.IP].dst)


def main(args):
    if len(args) < 2 or '--help' in args:
        print 'Usage: %s [--all | --ping | <path/to/recording.pcap>]' % args[0]

    elif args[1] == '--all':
        # Sniff all packets and display them nicely.
        S.sniff(prn=format_packet)

    elif args[1] == '--ping':
        # Sniff ping packets and print the result of parsing them.
        S.sniff(lfilter=packet_filter, prn=parse_packet)

    else:
        for packet in S.rdpcap(args[1]):
            print format_packet(packet)


def make_scapy_use_color():
    # When used in a regular script, scapy prints packets in one color. Using
    # this setting, we will make it print everything in color, which would be
    # much more readable :)
    import scapy.config
    import scapy.themes
    scapy.config.conf.color_theme = scapy.themes.DefaultTheme()


if __name__ == '__main__':
    import sys
    make_scapy_use_color()
    main(sys.argv)
