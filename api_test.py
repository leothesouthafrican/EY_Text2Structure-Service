import requests

# The endpoint URL
url = 'http://127.0.0.1:5003/parse-invoice'

# The path to the file you want to upload
file_path = '/workspaces/EY_Text2Structure-Service/invoice_text/dummy_text.txt'

# Open the file in binary mode
with open(file_path, 'rb') as file_to_upload:
    files = {
        'file': (file_path, file_to_upload)
    }

    # Send the POST request
    response = requests.post(url, files=files)

    # Check if the request was successful
    if response.status_code == 200:
        print('Success!')
        print(response.json())
    else:
        print('Failed!')
        print('Status Code:', response.status_code)
        print('Response Body:', response.text)
