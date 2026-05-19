def extract_metadata(packet):
    metadata = {}

    if packet.haslayer("IP"):
        metadata['src_ip'] = packet["IP"].src
        metadata['dst_ip'] = packet["IP"].dst

    if packet.haslayer("UDP"):
        metadata['src_port'] = packet["UDP"].sport
        metadata['dst_port'] = packet["UDP"].dport

    if packet.haslayer("Raw"):
        try:
            payload = packet["Raw"].load.decode(errors='ignore')
            if payload.startswith("SIP") or any(method in payload for method in ["INVITE", "BYE", "ACK", "REGISTER"]):
                lines = payload.split("\r\n")
                metadata['protocol'] = "SIP"
                metadata['sip_method'] = lines[0].split()[0] if lines else "UNKNOWN"
                for line in lines:
                    if line.startswith("From:"):
                        metadata['from'] = line
                    elif line.startswith("To:"):
                        metadata['to'] = line
                    elif line.startswith("Call-ID:"):
                        metadata['call_id'] = line
                metadata['sip_summary'] = f"{metadata.get('sip_method', 'UNKNOWN')} | {metadata.get('from', '')} → {metadata.get('to', '')}"
        except Exception:
            pass

    return metadata
