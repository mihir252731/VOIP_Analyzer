def parse_rtp(packet):
    if packet.haslayer('UDP'):
        udp = packet['UDP']
        if udp.dport >= 16384:
            print(f"[RTP?] Src Port: {udp.sport}, Dst Port: {udp.dport}")
            # Heuristics for RTP
