#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Generate fine activity news of region data from Google Custom Search API using filter with ChatGPT.
"""

from config import CHATGPT_API_KEY, PROMPT_GET_INDEX
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
# 検索結果のjsonファイルをarrayに変換
# @datafilepath arrayにするjsonファイル
#
def json2array(datafilepath):
	with open(datafilepath, 'r', encoding='utf-8') as fp:
		data = json.load(fp)
	
	rows = {}
	for p in data:
		rows[p] = []
		split_keyword = "ago ... "
		for item in data[p]:
			if "hours ago" in item['snippet']\
					or "hour ago" in item['snippet']\
					or "days ago" in item['snippet']\
					or "day ago" in item['snippet']:
				datetime_ago_text = item['snippet'].split(split_keyword)
				datetime_ago = datetime_ago_text[0]
				snippet = datetime_ago_text[1]
			else:
				datetime_ago = ""
				snippet = item['snippet']
			row = [p, item['title'], snippet, "", item['link'], datetime_ago]
			rows[p].append(row)

	return rows


#
# 検索結果から指定された都道府県のニュースをChatGPTで明るいニュースだけにふるいにかける
# @prefecture 都道府県名
# @data 検索結果データ
#
def get_finedata_index(prefecture, data):
	prompt = PROMPT_GET_INDEX.format(prefecture)
	prompt += "\n"

	prompt += '"""'
	for item in data:
		prompt += item[2] + "\n"
	prompt += '"""'

	chatgpt_response = do_prompt(prompt)

	return chatgpt_response


#
# プロンプトを実行
# @prompt プロンプト文字列
#
def do_prompt(prompt):
	client = OpenAI(
		api_key = CHATGPT_API_KEY
	)

	chat_completion = client.chat.completions.create(
		messages=[
			{
				"role": "user",
				"content": prompt,
			}
		],
		model="gpt-4o-mini",
	)
	return chat_completion


#
# 検索結果を明るい話題のみにフィルタリング
# @prefecture 都道府県
# @data 検索結果
#
def data_filtering(prefecture, data):
	chatgpt_response = get_finedata_index(prefecture, data[prefecture])
	indexes_str = chatgpt_response.choices[0].message.content.split(',')
	indexes = []
	for i in indexes_str:
		#print(prefecture, i, indexes_str)
		indexes.append(int(i))

	new_data = []
	#indexes = [2, 3, 5, 6, 8]
	# check たまに記事数を超えた数字をChatGPTが答えてくる
	for i in indexes:
		#print(prefecture, i, indexes)
		if type(i)==type(1) and 0<=i and i<len(indexes):
			new_data.append(data[prefecture][i])

	return new_data


#
# 検索結果をtsvに書き出し
# @data 検索結果
#
def write_tsv(data):
	with open("data.tsv", 'w', encoding='utf-8') as fp:
		for i in data:
			for row in data[i]:
				fp.write("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\n".format(row[0], row[1], row[2], row[3], row[4], row[5]))


def main():
	datafile = "test.json"
	all_data = json2array(datafile)
	write_tsv(all_data)
	exit()
	data = {}

    # filtering
	for p in PREFECTURES:
		tmp_data = data_filtering(p, all_data)
		data[p] = tmp_data

	# tmp write
	write_tsv(data)

	exit()

if __name__ == "__main__":
	main()
