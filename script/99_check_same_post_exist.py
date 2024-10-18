#
# Usage: python 99_check_same_post_exist.py <src1> <src2>
# src1とsrc2の行を比較して同じ行があるかどうかを確認するスクリプト

import sys

def main(src1=sys.argv[1], src2=sys.argv[2]):
    lines1 = []
    with open(src1, 'r', encoding='utf-8') as f:
        lines1 = f.readlines()

    lines2 = []
    with open(src2, 'r', encoding='utf-8') as f:
        lines2 = f.readlines()

    line_no = 1
    for l in lines1:
        if l in lines2:
            print(line_no, ": ", l)
        line_no += 1

main()
