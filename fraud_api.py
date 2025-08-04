
from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import joblib

app = Flask(__name__)
CORS(app)  # 👈 Must be placed right after app creation

model = joblib.load('fraud_rf_model.pkl')

@app.route('/')
def home():
    return "✅ Fraud Detection API is running!"


@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json

        milestones = data.get("milestones")  # list of dicts
        donation_amt = data.get("donation_amount")

        if not milestones or not donation_amt:
            return jsonify({"error": "Missing milestones or donation_amount"}), 400

        total_req = sum(m["Req"] for m in milestones)
        if total_req == 0:
            return jsonify({"error": "Total request cannot be 0"}), 400

        multiplier = donation_amt / total_req

        ml_input = {}
        for i, m in enumerate(milestones, 1):
            req_scaled = m["Req"] * multiplier
            exp_scaled = m["Exp"] * multiplier
            ml_input[f"Req_{i}"] = req_scaled
            ml_input[f"Exp_{i}"] = exp_scaled

        ml_input["Receipts_Uploaded"] = int(all(m["Receipts_Uploaded"] for m in milestones))

        ml_input["Deviation_1"] = ml_input["Req_1"] - ml_input["Exp_1"]
        ml_input["Deviation_2"] = ml_input["Req_2"] - ml_input["Exp_2"]
        ml_input["Deviation_3"] = ml_input["Req_3"] - ml_input["Exp_3"]

        features = [
            'Req_1', 'Exp_1','Deviation_1',
            'Req_2', 'Exp_2','Deviation_2',
            'Req_3', 'Exp_3','Deviation_3',
            'Receipts_Uploaded'
        ]

        df = pd.DataFrame([ml_input])
        prediction = model.predict(df[features])[0]

        explanation = ""
        if prediction == 1:
            explanation = "🚨 This NGO is flagged as potentially fraudulent due to unusual spending behavior."
        elif ml_input["Receipts_Uploaded"] == 0:
            explanation = "⚠️ Heads up! This NGO didn’t upload receipts, but their spending matches the donation milestones. We suggest caution or verifying before donating."
        else:
            explanation = "✅ This NGO's spending matches the expected milestones and receipts are uploaded."

        return jsonify({
            'is_fraud': int(prediction),
            'message': explanation,
            'ml_input': ml_input
        })

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
