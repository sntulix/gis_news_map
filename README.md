# 地域ごとのあかるいニュースマップ

地域ごとのニュースを収集してWebGISマップ上に表示するWebページを生成するスクリプトです。
leafletとOpenStreetMapを使用しています。
ニュースの収集にはGoogle Custom Search APIを使用しています。
あかるいニュースの振り分けにはChatGPT APIを利用しています。

# 使用方法

1. scriptディレクトリの1〜7までのスクリプトを順に実行してdata.jsonを生成
2. vite buildして生成したhtmlと一緒にWebサーバーにアップロードします。
