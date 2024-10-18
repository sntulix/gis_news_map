#
# Usage: python script/99_fix_json_utf.py src1.json dest.json
# JSONのマルチバイト文字が文字化けしている場合に修正するスクリプト
#
import json
import sys

def main(src1=sys.argv[1], dest=sys.argv[2]):
    with open(src1, 'r', encoding='utf-8') as f:
        src1_json = json.load(f)

    with open(dest, 'w', encoding='utf-8') as f:
        json.dump(src1_json, f, indent=4, ensure_ascii=False)

main()
