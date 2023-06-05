# https://0x2142.com/from-postman-to-python-your-first-get-request/

import requests
import json
import time

from cryptography.fernet import Fernet

key = b'6uNyOfjhKw8E2WwW2WQZ2rzQh0mkrNzXzf7KNLby9Zs='
fernet = Fernet(key)

ts = time.localtime()
tnow = time.strftime("%Y-%m-%d %H:%M:%S", ts)

print("Masukkan Suhu:")
input_suhu = input("> ") 
test=input_suhu+ "tubesPPLJ"
encData = fernet.encrypt(test.encode())

new_data = {
    "id_user": 1,
    "id_device": 1,
    "suhu": input_suhu,
}

# POST
# The API endpoint to communicate with
url_post = "http://192.168.43.79:8000/messages"

try:
    post_response = requests.post(url_post, json=new_data)
    # data = json.loads(post_response.text)
    post_response_json = post_response.json()
    print(post_response_json)
    # Process the JSON data
except json.JSONDecodeError as e:
    print(f"JSON decoding error: {e}")
    
# A POST request to tthe API
# post_response = requests.post(url_post, json=new_data)

# Print the response
# post_response_json = post_response.json()
# print(post_response_json)

# Print status code from original response (not JSON)
# print(post_response.status_code)

# GET
# The API endpoint
# url = "http://192.168.43.79:8000/messages"

# # A GET request to the API
# response = requests.get(url)

# # Print the response
# response_json = response.json()
# for response in response_json:
#     print(response['id_message'])
# print(response_json)
# print(response_json[0])