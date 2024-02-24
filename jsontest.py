print('Hello world!')

import json

with open('positions.json', 'rb') as a:
    print(json.load(a))


