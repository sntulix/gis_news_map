# 地域ごとのあかるいニュースマップ

## これは何ですか？

地域ごとのニュースを収集してWebGISマップ上に表示するWebページを生成するスクリプトです。
leafletとOpenStreetMapを使用しています。
ニュースの収集にはGoogle Custom Search APIを使用しています。
あかるいニュースの振り分けにはChatGPT APIを利用しています。

## 使用方法

1. scriptディレクトリの1〜7までのスクリプトを順に実行してdata.jsonを生成
2. vite buildして生成したhtmlと一緒にWebサーバーにアップロードします。

## About

This is a script generating news data each region and viewer html.
This uses Leaflet OpenStreetMap, Google Custom Search API, ChatGPT API.

## How to

1. Execute scripts 1 to 7 in script directory to generate data.json.
2. Generate the html by a command "vite build" and upload them to a Web Server.

## スクリーンショット / Screenshot

<img width="1240" alt="スクリーンショット" src="https://github.com/user-attachments/assets/afc91c26-b333-45b8-bd34-2d038c9882c5">

## 利用ライブラリ / Library

- [Vite](https://vite.dev)
- [Leaflet](https://leafletjs.com)
- [OpenStreetMap](https://www.openstreetmap.org/#map=5/35.59/134.38)
- [Google Custom Search API](https://developers.google.com/custom-search/v1/overview?hl=ja)
- [OpenAI ChatGPT API](https://platform.openai.com/docs/api-reference/introduction)
