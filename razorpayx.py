import requests
import json



url = "https://api.razorpay.com/v1/contacts"
data = {
  "name": "Ganesh Mahajan",
  "email": "ganeshmahajan1674@gmail.com",
  "contact":"+918530397730",
  "type":"employee",
  "reference_id":"Acme Contact ID 12345",
  "notes":{
    "notes_key_1":"Tea, Earl Grey, Hot",
    "notes_key_2":"Tea, Earl Grey… decaf."
  } 
}
headers = {
    "Content-Type": "application/json"
}
auth = ("rzp_test_7XJSI9QBxhtFSQ", "FGTnbTqN5gpIW9MVDJx9TAQJ")
response = requests.post(url, data=json.dumps(data), headers=headers, auth=auth)

print(response.status_code)
print(response.json())

