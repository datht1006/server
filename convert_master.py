import pandas as pd
import json

df = pd.read_excel("data/master.xlsx")

# chuẩn hóa tên cột
df.columns = df.columns.str.strip().str.lower()

result = []

for _, row in df.iterrows():
    result.append({
        "material": str(row.get("material", "")).strip(),
        "material_description": str(row.get("material description", "")).strip(),
        "basic_text": str(row.get("basic data text", "")).strip()
    })

with open("data/master.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print("✅ Convert xong master.json")