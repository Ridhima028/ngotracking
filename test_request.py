import requests

# Update with your local or Render URL
url = "http://127.0.0.1:5000/predict"

# Sample test input structured by milestone
data = {
   "donation_amount": 10000,
  "milestones": [
    { "Req": 5000, "Exp": 1000, "Receipts_Uploaded": 0 },
    { "Req": 3000, "Exp": 200, "Receipts_Uploaded": 0 },
    { "Req": 2000, "Exp": 100, "Receipts_Uploaded": 0 }
  ]
}

response = requests.post(url, json=data)

# Display response
if response.ok:
    res_json = response.json()
    print("🔍 Prediction:", "Fraud" if res_json["is_fraud"] == 1 else "Not Fraud")
    print("💬 Explanation:", res_json.get("message", "No explanation provided."))
    print("📊 ML Input Used:", res_json["ml_input"])
else:
    print("❌ Error:", response.text)
