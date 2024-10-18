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
	with open('links_per_prefecture.json', 'r', encoding='utf-8') as fp:
		datasources = json.load(fp)

	url_list = []
	url_with_latlng = {}
	for p in PREFECTURES:
		#print(p)
		for link in datasources[p]:
			if not link['url'] in url_list:
				url_list.append(link['url'])
	#print(len(url_list))
	link_count_per_prefecture = {}
	for url in url_list:
		link_count_per_prefecture[url] = 0

	for url in url_list:
		for p in PREFECTURES:
			for link in datasources[p]:
				if url==link['url']:
					link_count_per_prefecture[url] += 1
	#print(link_count_per_prefecture)

	for url in url_list:
		if 1 < link_count_per_prefecture[url]:
#			url_with_latlng[url] = {}
			for p in PREFECTURES:
				for link in datasources[p]:
					if url==link['url']:
						if not url in url_with_latlng:
							url_with_latlng[url] = {'title':link['title'], 'latlng':[]}
						url_with_latlng[url]['latlng'].append([PREFECTURES_LATLNG[p][0], PREFECTURES_LATLNG[p][1]])
			
	with open('link_network.json', 'w', encoding='utf-8') as fp:
		json.dump(url_with_latlng, fp, ensure_ascii=False, indent=2)

if __name__ == "__main__":
	main()
