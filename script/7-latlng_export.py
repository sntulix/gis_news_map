#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Generate fine activity news of region data from Google Custom Search API using filter with ChatGPT.
"""

__author__ = "Takahiro Shizuki (shizu@futuregadget.com)"

from prefecture_japan import PREFECTURES, PREFECTURES_NO, PREFECTURES_LATLNG

import pprint
import json
import re
import csv
import http.client
import urllib.parse
import time
from openai import OpenAI
from googleapiclient.discovery import build


def main():
	with open('chatgpt_responses.json', 'r', encoding='utf-8') as fp:
		data = json.load(fp)

	with open('links_per_prefecture_latlng.json', 'r', encoding='utf-8') as fp:
		datasources = json.load(fp)

	items = {}
	for p in PREFECTURES:
		items[p] = {}
		items[p]["prefecture"] = p
		items[p]["lat"] = PREFECTURES_LATLNG[p][0]
		items[p]["lng"] = PREFECTURES_LATLNG[p][1]
		items[p]["text"] = data[p].replace("\n\n", "<br>")
		items[p]["sources"] = datasources[p]

	with open('link_network.json', 'r', encoding='utf-8') as fp:
		link_network = json.load(fp)

	with open('data.json', 'w', encoding='utf-8') as fp:
		json.dump({'prefecture_info':items, 'region_network':link_network}, fp, ensure_ascii=False, indent=2)

if __name__ == "__main__":
	main()
