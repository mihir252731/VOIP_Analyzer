import os
from scapy.all import rdpcap
from extractor.metadata_extractor import extract_metadata
from analysis.threat_analysis import detect_threats
from analysis.rtp_analysis import analyze_rtp
from reporting.report_generator import generate_pdf_report

def analyze_pcap(pcap_path, output_pdf_path):
    print(f"\n[*] Analyzing: {pcap_path}")
    try:
        packets = rdpcap(pcap_path)
    except Exception as e:
        print(f"[!] Failed to read {pcap_path}: {e}")
        return

    metadata = []
    for pkt in packets:
        try:
            md = extract_metadata(pkt)
            if md and md.get("protocol") == "SIP":
                metadata.append(md)
        except Exception as e:
            print(f"[!] Metadata error in packet: {e}")

    threats = detect_threats(metadata)
    rtp_stats = analyze_rtp(packets)

    generate_pdf_report(metadata, threats, rtp_stats, output_file=output_pdf_path)

def main():
    pcap_folder = "data/captures"
    output_folder = "data/logs"
    os.makedirs(output_folder, exist_ok=True)

    for file in os.listdir(pcap_folder):
        if file.endswith(".pcap") or file.endswith(".pcapng"):
            pcap_path = os.path.join(pcap_folder, file)
            output_pdf = os.path.join(output_folder, f"{os.path.splitext(file)[0]}_report.pdf")
            analyze_pcap(pcap_path, output_pdf)

    print("\n[✔] Analysis complete for all files.")

if __name__ == "__main__":
    main()
