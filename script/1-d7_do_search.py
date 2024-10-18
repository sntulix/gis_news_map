#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Generate fine activity news of region data from Google Custom Search API using filter with ChatGPT.
"""

from config import GOOGLE_SEARCH_KEYWORD, GOOGLE_DEVELOPER_KEY, GOOGLE_SEARCH_CX, GOOGLE_SEARCH_LR, GOOGLE_SEARCH_DATERESTRICT, GOOGLE_SEARCH_SAFE, GOOGLE_START_MAX

from prefecture_japan import PREFECTURES, PREFECTURES_NO, PREFECTURES_LATLNG

__author__ = "Takahiro Shizuki (shizu@futuregadget.com)"

import pprint
import json
import re
import csv
import http.client
import urllib.parse
import time
from openai import OpenAI
from googleapiclient.discovery import build

#
# Google検索
# @keyword 検索ワード
#
def do_google_search(keyword, data_restrict="d7", result_start=1):
	# Build a service object for interacting with the API. Visit
	# the Google APIs Console <http://code.google.com/apis/console>
	# to get an API key for your own application.
	service = build(
		"customsearch", "v1", developerKey=GOOGLE_DEVELOPER_KEY
	)
	res = (
		service.cse()
		.list(
			q=keyword,
			cx=GOOGLE_SEARCH_CX,
			lr=GOOGLE_SEARCH_LR,
			dateRestrict=data_restrict, # GOOGLE_SEARCH_DATERESTRICT
			safe=GOOGLE_SEARCH_SAFE,
			start=result_start,
			filter=1,
		)
		.execute()
	)
	return res


#
# 経済ニュースを検索
# @datafilepath 保存パス
#
def do_search(datafilepath, search_keyword):
	search_result = {}
	result_start = 1
	page_max = GOOGLE_START_MAX
	for p in PREFECTURES:
		search_result[p] = []
		#print(p)
		for s in range(result_start, page_max, 10):
			# print("result_start:", s)
			result = do_google_search(search_keyword, data_restrict="d7", result_start=s)
			if result['searchInformation']['totalResults'] == '0':
				break
			search_result[p] += result['items']

	#write node
	with open(datafilepath, 'w', encoding='utf-8') as fp:
		json.dump(search_result, fp, ensure_ascii=False, indent=2)


def main():
	search_keyword = "能登"
	datafile = "test.json"
	do_search(datafile, search_keyword)


if __name__ == "__main__":
	main()
