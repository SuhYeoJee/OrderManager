import json

def tsv_to_json(tsv_str):
    lines = tsv_str.strip().split("\n")  # 줄 단위로 분리
    segment_keys = ["code", "name", "alias", "l", "t", "w","v", "bond", "concent", "specification"]
    keys = ["name", "seg1", "seg1_amount", "seg2", "seg2_amount", "shank","shank_amount", 
        "sub1", "sub1_amount", "sub2", "sub2_amount","paint","engrave","image","item_group"]

    result = []
    for line in lines:
        values = line.split("\t")  # 탭(\t)으로 분리
        data = dict(zip(keys, values))  # 키와 값 매핑
        data["seg1_amount"] = float(data["seg1_amount"]) if data["seg1_amount"] else 0
        data["seg2_amount"] = float(data["seg2_amount"]) if data["seg2_amount"] else 0
        data["shank_amount"] = float(data["shank_amount"]) if data["shank_amount"] else 0
        data["sub1_amount"] = float(data["sub1_amount"]) if data["sub1_amount"] else 0
        data["sub2_amount"] = float(data["sub2_amount"]) if data["sub2_amount"] else 0
        result.append(data)

    return result  # JSON 변환 없이 리스트 반환

# 예제 TSV 문자열
tsv_str = """
3"6OR60CW	SQ0081	6			3"DISC-SSCW	1					ORANGE	O60		3"6OR60
"""

# JSON 변환
json_data = tsv_to_json(tsv_str)

# JSON 파일 저장
with open("tip_tsv_to_db.json", "w", encoding="utf-8") as f:
    json.dump(json_data, f, ensure_ascii=False, indent=4)
