import requests
response = requests.get("https://mkwrs.com/mk8dx/")
print(response.status_code)
print(response.content)
