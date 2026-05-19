import os
from scapy.all import sniff, wrpcap

def capture_voip_packets(output_file='data/captures/voip_traffic.pcap',
                         iface='\\Device\\NPF_{F2BE3797-EC55-43B1-83DB-1A7D8BA2D82B}',
                         filter='udp or tcp port 5060'):

    # ✅ Create directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    print(f"[*] Capturing packets on {iface} with filter: {filter}")
    packets = sniff(iface=iface, filter=filter, timeout=60)
    wrpcap(output_file, packets)
    print(f"[+] Packets saved to {output_file}")
