from rapidfuzz import fuzz
from utils.normalize import normalize

def similarity(a, b):
    return fuzz.token_sort_ratio(a, b) / 100


def compare_items(input_data, master_data):
    results = []

    for item in input_data:
        text_input = normalize(item.get("ten_chuan") or item.get("ten_goc") or "")

        if not text_input:
            continue

        best_match = None
        best_score = 0

        for m in master_data:
            search_text = m.get("search_text", "")

            # 🚀 filter nhanh
            if text_input[:5] not in search_text:
                continue

            score = similarity(text_input, search_text)

            if score > best_score:
                best_score = score
                best_match = m

            # 🚀 early stop
            if best_score > 0.95:
                break

        results.append({
            "row_excel": item.get("row_excel"),
            "ten_goc": item.get("ten_goc"),
            "ten_chuan": item.get("ten_chuan"),
            "match": best_match.get("material_description") if best_match else "",
            "basic": best_match.get("basic") if best_match else "",
            "material_description": best_match.get("material_description") if best_match else "",
            "score": round(best_score, 2),
            "status": "OK" if best_score > 0.85 else "ERROR"
        })

    return results