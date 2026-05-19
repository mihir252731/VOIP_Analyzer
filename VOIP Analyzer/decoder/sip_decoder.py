def parse_sip_packet(packet):
    if packet.haslayer('Raw'):
        payload = str(packet['Raw'].load)
        if "SIP" in payload or "INVITE" in payload:
            print("[SIP] Packet found")
            lines = payload.split("\\r\\n")
            for line in lines:
                if line.startswith(("From:", "To:", "Call-ID:", "CSeq:", "Via:")):
                    print(f"   {line}")
