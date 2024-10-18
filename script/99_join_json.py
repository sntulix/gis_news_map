#
# Usage: python script/99_join_json.py src1 src2 dest
# src1にsrc2を都道府県別に結合、同じリンクがある場合はそのリンクは結合しない（重複させない）
#

import json
import sys

def join_json(src1, src2):
    with open(src1, 'r', encoding='utf-8') as f:
        src1_json = json.load(f)
    with open(src2, 'r', encoding='utf-8') as f:
        src2_json = json.load(f)

    for prefecture in src2_json:
        duplicate_count = 0
        for item2 in src2_json[prefecture]:
            has_item = False
            for item1 in src1_json[prefecture]:
                if item2['link'] == item1['link']:
                    has_item = True
                    break
            if has_item:
                duplicate_count += 1
                print("find a dupulicate:", item2['link'])
                if "https://www.tokyo-np.co.jp/article/355641" in item2['link']:
                    print("\t", item2['title'])
                if "石川県能登地方に大雨特別警報 最大級" in item2['title']:
                    print("\t", item2['title'])
            else:
                src1_json[prefecture].append(item2)
        print(prefecture, "duplicate count:", duplicate_count)
    return src1_json

def main(src1=sys.argv[1], src2=sys.argv[2], dest=sys.argv[3]):
    with open(dest, 'w', encoding='utf-8') as f:
        json.dump(join_json(src1, src2), f, indent=4, ensure_ascii=False)

main()
