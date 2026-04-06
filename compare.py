from rapidfuzz import fuzz
from utils.normalize import normalize

def similarity(a, b):
    return fuzz.token_sort_ratio(a, b) / 100


def compare_items(input_data, master_data):
    results = []

    for item in input_data:
        # Ưu tiên ten_vat_tu_chuan, fallback ten_goi_vat_tu
        text_input = normalize(
            item.get("ten_vat_tu_chuan") or item.get("ten_goi_vat_tu") or ""
        )

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

        # ===== Giữ lại TẤT CẢ fields từ parser + thêm kết quả match =====
        record = {**item}  # copy toàn bộ fields từ Excel

        record.update({
            "material_description": best_match.get("material_description", "") if best_match else "",
            "basic":                best_match.get("basic", "") if best_match else "",
            "score":                round(best_score, 2),
            "status":               "OK" if best_score > 0.85 else "ERROR",
        })

        results.append(record)

    return results