import requests

url = "http://127.0.0.1:8000/start"

# גוף הבקשה – JSON
payload = {"data":
               {"test": "kjdskjdskjdsk"}
}

# שליחת POST
response = requests.post(url, json=payload)

# הדפסת תשובה מהשרת
print("Status:", response.status_code)
print("Response:", response.json())
