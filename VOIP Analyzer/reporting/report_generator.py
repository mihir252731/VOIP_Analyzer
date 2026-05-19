from fpdf import FPDF
import os
import re

def clean(text):
    return re.sub(r'[^\x00-\x7F]', '?', str(text))

def generate_pdf_report(metadata_list, threats, rtp_stats, output_file='data/logs/voip_report.pdf'):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, "VoIP Traffic Analysis Report", ln=True, align='C')
    pdf.ln(10)

    # SIP Summary
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, "SIP Traffic Summary", ln=True)
    pdf.set_font("Arial", size=11)
    pdf.cell(200, 10, f"Total SIP Packets: {len(metadata_list)}", ln=True)
    pdf.ln(4)

    for md in metadata_list:
        pdf.multi_cell(0, 6, clean(md.get("sip_summary", "Unknown")))

    # RTP Summary
    pdf.ln(6)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, "RTP Stream Summary", ln=True)
    pdf.set_font("Arial", size=11)
    if not rtp_stats:
        pdf.cell(200, 10, "No RTP traffic detected.", ln=True)
    else:
        for stat in rtp_stats:
            pdf.multi_cell(0, 6, clean(
                f"SSRC: {stat['ssrc']} | Packets: {stat['packets']} | Lost: {stat['lost']} | "
                f"Jitter: {stat['jitter']} | Codec: {stat['codec']} | Avg Payload: {stat['avg_payload']}B"
            ))

    # Threat Summary
    pdf.ln(6)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, "Detected SIP Threats", ln=True)
    pdf.set_font("Arial", size=11)
    if not threats:
        pdf.cell(200, 10, "No SIP threats detected.", ln=True)
    else:
        for t in threats:
            pdf.multi_cell(0, 6, clean(f"{t['type']}: {t['details']}"))

    pdf.output(output_file)
    print(f"[✔] Report saved to {output_file}")
