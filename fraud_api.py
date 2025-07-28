from flask import Flask, request, jsonify
import pandas as pd
import joblib

app = Flask(__name__)
model = joblib.load('fraud_rf_model.pkl')

@app.route('/')
def home():
    return "✅ Fraud Detection API is running!"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        df = pd.DataFrame([data])

        # Feature engineering
        df['Deviation_1'] = df['Req_1'] - df['Exp_1']
        df['Deviation_2'] = df['Req_2'] - df['Exp_2']
        df['Deviation_3'] = df['Req_3'] - df['Exp_3']
        df['Total_Requested'] = df['Req_1'] + df['Req_2'] + df['Req_3']
        df['Total_Used'] = df['Exp_1'] + df['Exp_2'] + df['Exp_3']
        df['Total_Deviation'] = df['Total_Requested'] - df['Total_Used']
        df['Deviation_Percent'] = (df['Total_Deviation'] / (df['Total_Requested'] + 1)) * 100

        df['req_diff_1_2'] = df['Req_2'] - df['Req_1']
        df['req_diff_2_3'] = df['Req_3'] - df['Req_2']

        # Feature order for model
        features = [
            'Req_1', 'Exp_1', 'Deviation_1',
            'Req_2', 'Exp_2', 'Deviation_2',
            'Req_3', 'Exp_3', 'Deviation_3',
            'Receipts_Uploaded'
        ]
        df_model = df[features]

        # Predict fraud
        prediction = model.predict(df_model)[0]

        # Build explanation
        reasons = []

        if df['Deviation_Percent'][0] > 80:
            reasons.append("Deviation Percent is above 80%")
        elif df['Deviation_Percent'][0] > 50:
            reasons.append("Deviation Percent is above 50%")

        if df['Receipts_Uploaded'][0] == 0:
            reasons.append("Missing receipts")

        for i in [1, 2, 3]:
            if df[f'Deviation_{i}'][0] > 1000:
                reasons.append(f"Large expense deviation in Phase {i}")

        if (df['req_diff_1_2'][0] > 2000) or (df['req_diff_2_3'][0] > 2000):
            reasons.append("Non-linear request jump between phases")

        return jsonify({
            'is_fraud': int(prediction),
            'reasons': reasons if prediction == 1 else []
        })

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
