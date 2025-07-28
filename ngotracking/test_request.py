import requests

# Replace with your actual server URL if deployed (e.g., on Heroku)
url = "http://127.0.0.1:5000/predict"

# Sample test input data (replace with different test cases as needed)
data = {
    "Req_1": 10000, "Exp_1": 100,
    "Req_2": 5000, "Exp_2": 500,
    "Req_3": 2000, "Exp_3": 200,
    "Receipts_Uploaded": 0
}

# Make POST request to the API
response = requests.post(url, json=data)

# Print the response from the API
print("API Response:", response.json())
