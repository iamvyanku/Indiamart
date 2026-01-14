from flask import Flask, request, jsonify
import pandas as pd
import os
from datetime import datetime

app = Flask(__name__)

CSV_FILE = "indiamart_leads.csv"

# ---------------------------------
# Utility: Save Lead to CSV
# ---------------------------------
def save_to_csv(data):
    lead = {
        "name": data.get("sender_name", ""),
        "mobile": data.get("sender_mobile", ""),
        "email": data.get("sender_email", ""),
        "company": data.get("company_name", ""),
        "product": data.get("product_name", ""),
        "message": data.get("enquiry_message", ""),
        "city": data.get("city", ""),
        "state": data.get("state", ""),
        "enquiry_time": data.get("enquiry_time", ""),
        "received_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    df = pd.DataFrame([lead])

    # Append safely (create file if not exists)
    if os.path.exists(CSV_FILE):
        df.to_csv(CSV_FILE, mode="a", header=False, index=False)
    else:
        df.to_csv(CSV_FILE, mode="w", header=True, index=False)


# ---------------------------------
# Webhook Endpoint
# ---------------------------------
@app.route("/indiamart/webhook", methods=["POST"])
def indiamart_webhook():
    print("✅ Webhook HIT", flush=True)

    data = request.get_json(force=True, silent=True)
    print("📥 Raw data:", data, flush=True)

    if not data or not data.get("sender_mobile"):
        return jsonify({"error": "Invalid payload"}), 400

    save_to_csv(data)
    print("📥 Lead stored:", data, flush=True)

    return jsonify({"status": "stored"}), 200

# if __name__ == "__main__":
#     app.run(port=5000)
from flask import send_file

@app.route("/download/csv", methods=["GET"])
def download_csv():
    if not os.path.exists("indiamart_leads.csv"):
        return jsonify({"error": "CSV file not found"}), 404

    return send_file(
        "indiamart_leads.csv",
        as_attachment=True,
        download_name="indiamart_leads.csv"
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

