#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Generate fine activity news of region data from Google Custom Search API using filter with ChatGPT.
"""

from config import PROMPT_GET_SUMMARY, CHATGPT_API_KEY
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
# ChatGPTに渡すプロンプトを作成
# @prefecture 都道府県
# @data 検索結果データ
#
def get_prompt(prefecture, data):
	prompt = PROMPT_GET_SUMMARY.format(prefecture)
	prompt += "\n"

	prompt += '"""'
	for item in data:
		prompt += item[0] + ":" + item[1] + ":" + item[2]  + ":" + item[5] + "\n"
	prompt += '"""'

	return prompt


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
# 地域ごとのデータの要約をChatGPTで生成
#
def get_summary(p, data):
	prompt = get_prompt(p, data)
	#print(prompt)	
	chatgpt_response = do_prompt(prompt)
	#print(chatgpt_response)
	return chatgpt_response.choices[0].message.content


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

	# get summary by chatgpt
	responses = {}
	for p in PREFECTURES:
		chatgpt_response = get_summary(p, data[p])
		responses[p] = chatgpt_response

	with open('chatgpt_responses.json', 'w', encoding='utf-8') as fp:
		json.dump(responses, fp, ensure_ascii=False, indent=2)


if __name__ == "__main__":
	main()
