# Google Custom Search API
GOOGLE_SEARCH_KEYWORD = "能登"
GOOGLE_DEVELOPER_KEY = ""
GOOGLE_SEARCH_CX = ""
GOOGLE_SEARCH_LR = "lang_ja"
GOOGLE_SEARCH_DATERESTRICT = "d1" # 過去7日分
GOOGLE_SEARCH_SAFE = "active"
GOOGLE_START_MAX = 100

# 都道府県とまぎらわしい場所表記は使わない
NOT_SHOW_ADDRESS = ["都道府県",
                    "同市","同県","同町",
                    "首都","市町","市区","市町村","市区町村",
                    "圏央道","国道","鉄道",
                    "大都市","労働市","経済県都",
                    "学校法人京都",]

# NGワード
#NOT_SHOW_THEME = ["逮捕", "訃報", "不適切", "死去", "クマ目撃", "アラート", "群馬県警", "座席蹴る", "原発"]
NOT_SHOW_THEME = []

# ChatGPT
CHATGPT_API_KEY = ""
PROMPT_GET_INDEX = "これは{0}の今週のニュースです。これらからこの地域のこれまで積み重ねられてきたこと、これから生まれること、あかるいきざしを行番号で答えてください。カンマ区切りの数字並びにして返してもらえますか？ 0から数えてください。番号のみ答えてください"
PROMPT_GET_SUMMARY = "これは{0}の今週のニュースです。これを元にこの地域経済のあかるいニュースのみ教えてもらえますか？ また、固有名詞は書かずにお願いします。50文字以内でお願いします。"

