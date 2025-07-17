import requests

url = "http://127.0.0.1:5000/predict"

data = {
    "Req_1": 10000,
    "Exp_1": 10000,   
    "Req_2": 5000,
    "Exp_2": 50,
    "Req_3": 3000,
    "Exp_3": 30,
    "Receipts_Uploaded": 1

}


response = requests.post(url, json=data)
print("API Response:", response.json())


