import requests
import json

info = requests.get('https://api.github.com/user/repos', auth = ('alscovidny', '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'))

repos = info.json()
a = list()

for repo in repos:
  a.append({'name' : repo['name']})

with open ('data.json', 'w') as f:
    json.dump(a, f, indent = 4)