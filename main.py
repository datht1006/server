from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import json
import os
import asyncio

from parser import parse_2_columns
from compare import compare_items

app = FastAPI()

# ===== CORS =====
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== LOAD MASTER =====
def preprocess_master(master_data):
    from utils.normalize import normalize

    for m in master_data:
        desc = m.get("material_description", "")
        basic = m.get("basic", "")
        m["search_text"] = normalize(f"{desc} {basic}")

    return master_data


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MASTER_PATH = os.path.join(BASE_DIR, "data", "master.json")

with open(MASTER_PATH, "r", encoding="utf-8") as f:
    MASTER_DATA = preprocess_master(json.load(f))


# ===== API =====
@app.get("/")
def root():
    return {"status": "ok"}


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        # 🔥 đọc file async (tránh block)
        contents = await file.read()

        # 👉 ghi ra temp file để parser đọc
        temp_path = "temp.xlsx"
        with open(temp_path, "wb") as f:
            f.write(contents)

        # 👉 chạy parsing ở thread riêng (tránh block CPU)
        input_data = await asyncio.to_thread(parse_2_columns, temp_path)

        print("INPUT:", len(input_data))
        print("MASTER:", len(MASTER_DATA))

        # 👉 compare cũng chạy thread
        result = await asyncio.to_thread(compare_items, input_data, MASTER_DATA)

        # 👉 xóa file temp
        os.remove(temp_path)

        return {
            "success": True,
            "total": len(result),
            "error_count": sum(1 for r in result if r["status"] == "ERROR"),
            "data": result
        }

    except Exception as e:
        print("ERROR:", str(e))
        return {
            "success": False,
            "error": str(e)
        }


# ===== RUN LOCAL =====
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)

