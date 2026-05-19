from scapy.all import IP, UDP

def is_voip_packet(packet):
    if IP in packet and UDP in packet:
        dport = packet[UDP].dport
        return dport == 5060 or (16384 <= dport <= 32767)
    return False

def safe_get(layer, field, default='N/A'):
    try:
        return getattr(layer, field)
    except AttributeError:
        return default
