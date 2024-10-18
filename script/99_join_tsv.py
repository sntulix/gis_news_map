#
# Usage: python script/99_join_tsv.py src1 src2 dest
# src1にsrc2を都道府県別に結合、同じリンクがある場合はそのリンクは結合しない（重複させない）
#

import json
import sys

def join_tsv(src1, src2):
    src1_list = []
    src2_list = []
    new_list = []
    with open(src1, 'r', encoding='utf-8') as f:
        src1_list = f.readlines()
    with open(src2, 'r', encoding='utf-8') as f:
        src2_list = f.readlines()

    duplicate_count = 0
    for item2 in src2_list:
        has_item = False
        for item1 in src1_list:
            if item2 == item1:
                print("find a dupulicate")
                duplicate_count += 1
                has_item = True
                break
        if has_item == False:
            new_list.append(item2)
    print("duplicate count:", duplicate_count)
    return new_list

def main(src1=sys.argv[1], src2=sys.argv[2], dest=sys.argv[3]):
    with open(dest, 'w', encoding='utf-8') as f:
        f.writelines(join_tsv(src1, src2))

main()
