from flask import Flask, render_template, jsonify
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "VoIP Analysis Dashboard (Coming Soon...)"

@app.route('/api/threats')
def get_threats():
    # Placeholder: Load from analysis results
    return jsonify([
        {"type": "SIP Flood", "source": "192.168.1.20"},
        {"type": "RTP anomaly", "stream": "Call ID 12345"}
    ])

if __name__ == "__main__":
    app.run(debug=True)
