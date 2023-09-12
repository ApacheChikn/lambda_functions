import requests

x = requests.get('https://79i3buwfdl.execute-api.us-east-1.amazonaws.com/')
print(x.status_code)

#%%

print(type(x))
print(dir(x))

#%%

response_json = x.json()

#%%

import json
response_json_loaded = json.loads(response_json["body"])

#%%

for bucket in response_json_loaded:
    print(bucket)