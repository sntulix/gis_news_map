#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Generate fine activity news of region data from Google Custom Search API using filter with ChatGPT.
"""

from config import NOT_SHOW_ADDRESS
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


#
# 住所を取得
# @prefecture 都道府県
# @text テキストから住所列を取得
#
def get_address(prefecture, text):
	from_code = b'\xe3\x83\xbd'.decode('utf-8')
	to_code = b'\xe9\xbe\xa0'.decode('utf-8')
	result = re.findall(r'[' + from_code + '-' + to_code + ']+[都道府県市区町村]', text)
	address = result
	if len(address)==0:
		address = [prefecture]
	#print(address)
	return address


#
# 住所を取得してジオコーディングする
# @data 検索結果
#
def do_get_address(data):
	# get address
	data_with_address = {}
	for p in data:
		data_with_address[p] = []
		for item in data[p]:
			if item[3]=="": # 非表示フラグに何もなければ実施
				address = get_address(p, item[2])
				if not address==None:
					address = set(address)
					# 見出しにある住所の分だけくり返す
					for a in address:
						#print(a)
						# 都道府県とまぎらわしい場所表記は使わない
						# 見出しの持つ住所が複数で、都道府県名と同じ住所の場合は重複しないように含まない
						if a in NOT_SHOW_ADDRESS:
							continue
						if len(address)>1 and a==p:
							continue

						address_latlng = [0,0]
						if not p in a:
							# 見出しの持つ住所が都道府県名でない場合は、ジオコーディングの住所にキーになっている都道府県を加えてジオコーディングする
							address_latlng = do_geocoding(p, p+a)
						else:
							address_latlng = do_geocoding(p, a)
						# API呼び出しにwaitをかけておく
						time.sleep(0.1)
						#print(address_latlng)
						# 緯度軽度を加えて新たにデータ配列を作り直す
						data_with_address[p].append([
							item[0], item[1],
							a,
							address_latlng[0], address_latlng[1],
							item[2], item[3], item[4]]
						)
	return data_with_address


#
# ジオコーディングをする
# @prefecture 都道府県
# 住所
#
def do_geocoding(prefecture, address):
	host = "msearch.gsi.go.jp"
	conn = http.client.HTTPSConnection(host)
	param = urllib.parse.urlencode({'q':address})
	conn.request("GET", "/address-search/AddressSearch?"+param, headers={"Host": host})
	response = conn.getresponse()
	#print(response.status, response.reason)
	result = response.read().decode()
	#print(result)
	json_data = json.loads(result)
	#print(json_data[0].coordinates)
	if len(json_data)>0:
		return json_data[0]["geometry"]["coordinates"]
	else:
		host = "msearch.gsi.go.jp"
		conn = http.client.HTTPSConnection(host)
		param = urllib.parse.urlencode({'q':prefecture})
		conn.request("GET", "/address-search/AddressSearch?"+param, headers={"Host": host})
		result = conn.getresponse().read().decode()
		json_data = json.loads(result)
		return json_data[0]["geometry"]["coordinates"]
	

def main():
	data = {}
	with open('data.tsv', newline='', encoding='utf-8') as csvfile:
		reader = csv.reader(csvfile, delimiter='\t')
		for row in reader:
			if not row[0] in data:
				data[row[0]] = []
				data[row[0]].append(row)
			else:
				data[row[0]].append(row)

	# get address
    # ジオコーディングする
    # リンクの見出しにある地域の分だけリンクを増幅させる
	data_with_address = do_get_address(data)
	
	# tmp write
	write_data_with_address_tsv(data_with_address)


if __name__ == "__main__":
	main()
