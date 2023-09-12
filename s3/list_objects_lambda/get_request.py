import requests

url = 'https://tvk3opnmbe.execute-api.us-east-1.amazonaws.com/prod?bucket_name={}'
bucket_name = 'zali-catch-all'

x = requests.get(url.format(bucket_name))
print(x.status_code)

#%%

print(type(x))

#%%

response_json = x.json()

for object in response_json:
    print(object)
