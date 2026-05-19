from collections import defaultdict

def is_rtp_packet(pkt):
    if pkt.haslayer("UDP") and hasattr(pkt["UDP"], "payload"):
        payload = bytes(pkt["UDP"].payload)
        if len(payload) > 12:
            version = payload[0] >> 6
            payload_type = payload[1] & 0x7F
            if version == 2 and 0 <= payload_type <= 127:
                return True
    return False

def analyze_rtp(packets):
    rtp_info = defaultdict(list)
    for pkt in packets:
        if pkt.haslayer("IP") and is_rtp_packet(pkt):
            ip = pkt["IP"]
            udp = pkt["UDP"]
            payload = bytes(udp.payload)
            if len(payload) < 12:
                continue
            seq = int.from_bytes(payload[2:4], byteorder="big")
            timestamp = int.from_bytes(payload[4:8], byteorder="big")
            ssrc = int.from_bytes(payload[8:12], byteorder="big")
            size = len(payload)
            rtp_info[ssrc].append((seq, timestamp, size))

    rtp_summary = []

    for ssrc, packets in rtp_info.items():
        packets.sort()
        seq_nums = [p[0] for p in packets]
        timestamps = [p[1] for p in packets]
        sizes = [p[2] for p in packets]

        total = len(seq_nums)
        expected = (max(seq_nums) - min(seq_nums) + 1) if seq_nums else 0
        lost = max(0, expected - total)
        jitter = max(
            [abs(timestamps[i] - timestamps[i-1]) for i in range(1, len(timestamps))],
            default=0
        )
        avg_payload = sum(sizes) // len(sizes) if sizes else 0
        codec = "G.711" if avg_payload == 160 else "Unknown"

        rtp_summary.append({
            "ssrc": ssrc,
            "packets": total,
            "expected": expected,
            "lost": lost,
            "jitter": jitter,
            "avg_payload": avg_payload,
            "codec": codec
        })

    return rtp_summary
