import sys
import json

with open(sys.argv[1], 'r', encoding='utf-8') as f:
    lines = f.readlines()

    prefectures = {}
    for line in lines:
        items = line.split("\t")
        prefectures[items[0]] = []

    for line in lines:
        words = line.split("\t")
        item = {'title': words[1], 'link': words[3], 'snippet': words[2]}
        prefectures[words[0]].append(item)

#print(prefectures)
with open(sys.argv[2], 'w', encoding='utf-8') as f:
    f.write(json.dumps(prefectures, ensure_ascii=False, indent=2))