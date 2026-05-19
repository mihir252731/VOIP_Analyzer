def detect_threats(metadata_list):
    threats = []
    seen_calls = set()

    for meta in metadata_list:
        if meta.get("protocol") == "SIP":
            call_id = meta.get("call_id", "UNKNOWN")
            method = meta.get("sip_method", "UNKNOWN")

            # Basic threat logic
            if method == "BYE" and call_id not in seen_calls:
                threats.append({
                    "type": "Anomalous BYE",
                    "details": f"BYE without matching INVITE (Call-ID: {call_id})"
                })

            if method == "INVITE":
                seen_calls.add(call_id)

    return threats
