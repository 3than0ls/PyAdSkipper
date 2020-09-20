import json
import os

with open('datas.json', 'w') as f:
    json.dump(dict(os.environ), f, indent=4)