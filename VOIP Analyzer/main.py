from capture.packet_sniffer import capture_voip_packets
from decoder.sip_decoder import parse_sip_packet
from scapy.all import rdpcap

if __name__ == "__main__":
    capture_voip_packets()
    packets = rdpcap('data/captures/voip_traffic.pcap')
    for pkt in packets:
        parse_sip_packet(pkt)
