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
    data = request.json
    df = pd.DataFrame([data])

    df['Deviation_1'] = df['Req_1'] - df['Exp_1']
    df['Deviation_2'] = df['Req_2'] - df['Exp_2']
    df['Deviation_3'] = df['Req_3'] - df['Exp_3']

    if ((df['Deviation_1'][0] > 500) or
        (df['Deviation_2'][0] > 500) or
        (df['Deviation_3'][0] > 500) or
        (df['Receipts_Uploaded'][0] == 0)):
        return jsonify({'is_fraud': 1})
    
    return jsonify({'is_fraud': 0})


if __name__ == '__main__':
    app.run(debug=True)
