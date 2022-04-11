import requests
from pprint import pprint

access_token = '5d229e417e40c76eef8f18a2e615829158303db491602481b7f0f064641169f25b08d32cd15d0ff28f423'
user_id = '316672547'
extended = 1

info = requests.get(f'https://api.vk.com/method/users.getSubscriptions?user_id={user_id}\
&extended={extended}&access_token={access_token}&v=5.131')

pprint(info.json())
