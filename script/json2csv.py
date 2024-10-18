import json

def getItemInfo(item):
    return {'snippet':item['snippet'],
            'link':item['link'],
            }

def json2csv(json_file, csv_file):
    with open(json_file, 'r') as f:
        data = json.load(f)

    with open(csv_file, 'w') as f:
        f.write("snippet,link" + '\n')
        for item in data['items']:
            item_info = getItemInfo(item)
            print(item_info)
            f.write(','.join(item_info.values()) + '\n')

json2csv('test.json', 'data.csv')

