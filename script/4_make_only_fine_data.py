#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Generate fine activity news of region data from Google Custom Search API using filter with ChatGPT.
"""

from config import NOT_SHOW_THEME
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
# tsvを住所つきで書き出し
# @data 検索結果
#
def write_data_with_address_tsv(data):
	with open("data_with_address.tsv", 'w', encoding='utf-8') as fp:
		for i in data:
			for row in data[i]:
				fp.write("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\n".format(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))


def create_datalist_by_address(datasources):
	# 住所でまとめる
	address_list = []
	datasources_by_prefecture_address_list = {}
	for p in PREFECTURES:
		# 住所リストを作る
		for item in datasources[p]:
			if not item['address'] in address_list:
				address_list.append(item['address'])
		# print(address_list)

		# 住所の重複、部分一致を削除
		remove_list = []
		for address in address_list:
			for add2 in address_list:
				if address in add2:
					if len(add2)<len(address):
						if not add2 in remove_list:
							remove_list.append(add2)
					elif len(add2)>len(address):
						if not address in remove_list:
							remove_list.append(address)
		# print(remove_list)
		for r in remove_list:
			address_list.remove(r)
		# print(address_list)

		# 住所リストを元に、都道府県-住所でデータをまとめる
		# cnt = 0
		datasources_by_prefecture_address_list[p] = {}
		for item in datasources[p]:
			# print(len(datasources[p]))
			# print(item['address'])
			# 住所キーを探す
			address_key = item['address']
			# for address_key_base in address_list:
			# 	if item['address'] in address_key_base:
			# 		address_key = address_key_base
			# 		break
			# print("address_key", address_key)
			if not address_key in datasources_by_prefecture_address_list[p]:
				datasources_by_prefecture_address_list[p][address_key] = {
					'lat':item['lat'], 'lng':item['lng'], 'sources': []
				}
			# print(item['title'])
			datasources_by_prefecture_address_list[p][address_key]['sources'].append(
				{'title':item['title'], 'url':item['url']}
			)

def main():
	data = {}
	with open('data_with_address.tsv', newline='', encoding='utf-8') as csvfile:
		reader = csv.reader(csvfile, delimiter='\t')
		for row in reader:
			if not row[0] in data:
				data[row[0]] = []
				data[row[0]].append(row)
			else:
				data[row[0]].append(row)
	datasources = {}
	for p in PREFECTURES:
		datasources[p] = []
		added_list = []
		if not p in data:
			continue
		for item in data[p]:
			# print(item)
			skip_flag = False
			# 明るくなさそうなワードがある記事は含まない
			for word in NOT_SHOW_THEME:
				if word in item[1]:
					skip_flag = True
					break
			if skip_flag == True:
				continue
			datasources[p].append({'title':item[1], 'url':item[6], 'address':item[2], 'lat':item[4], 'lng':item[3]})
#			if not item[1] in added_list:
#				datasources[p].append({'title':item[1], 'url':item[6], 'lat':item[3], 'lang':item[4]})
#				added_list.append(item[1])

	# 緯度軽度でまとめる
	latlng_list = []
	datasources_by_prefecture_latlng_list = {}
	for p in PREFECTURES:
		# 住所リストを作る
		for item in datasources[p]:
			if not item['lat']+item['lng'] in latlng_list:
				latlng_list.append(item['lat']+item['lng'])
		# print(address_list)

		# 緯度軽度リストを元に、都道府県-緯度軽度でデータをまとめる
		# cnt = 0
		datasources_by_prefecture_latlng_list[p] = {}
		for item in datasources[p]:
			# print(len(datasources[p]))
			# 住所キーを探す
			latlng_key = item['lat']+item['lng']
			# print(latlng_key)
			# latlngをキーにして要素を作る
			if not latlng_key in datasources_by_prefecture_latlng_list[p]:
				datasources_by_prefecture_latlng_list[p][latlng_key] = {
					'title':item['address'], 'lat':item['lat'], 'lng':item['lng'], 'sources': []
				}
			else:
				# 見出しに含まれていない住所を追加
				if not item['address'] in datasources_by_prefecture_latlng_list[p][latlng_key]['title']:
					datasources_by_prefecture_latlng_list[p][latlng_key]['title'] += "、"+item['address']
			# print(item['title'])
			# 都道府県-緯度軽度リストになければ、記事を追加
			has_link = False
			for source in datasources_by_prefecture_latlng_list[p][latlng_key]['sources']:
				if source['url'] == item['url']:
					has_link = True
					break
			if not has_link:
				datasources_by_prefecture_latlng_list[p][latlng_key]['sources'].append(
					{'title':item['title'], 'url':item['url']}
				)

	with open("links_per_prefecture_latlng.json", "w", encoding='UTF-8') as fp:
		json.dump(datasources_by_prefecture_latlng_list, fp, ensure_ascii=False, indent=2)


if __name__ == "__main__":
	main()
