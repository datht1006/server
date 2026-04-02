import pandas as pd

def parse_2_columns(file_obj):
    raw = pd.read_excel(file_obj, header=None)

    # tìm header
    header_row = None
    for i in range(20):
        row = raw.iloc[i].astype(str).str.lower()

        if row.str.contains("tên gọi vật tư").any():
            header_row = i
            break

    if header_row is None:
        raise ValueError("Không tìm thấy header")

    # đọc lại với header đúng
    df = pd.read_excel(file_obj, header=header_row)
    df.columns = df.columns.astype(str).str.strip().str.lower()

    col_goc = None
    col_chuan = None

    for col in df.columns:
        if "tên gọi vật tư" in col:
            col_goc = col
        elif "chuẩn hóa" in col:
            col_chuan = col

    if not col_goc or not col_chuan:
        raise ValueError("Không tìm thấy 2 cột cần thiết")

    result = []

    for i, row in df.iterrows():
        ten_goc = str(row[col_goc]).strip()
        ten_chuan = str(row[col_chuan]).strip()

        if ten_goc.lower() in ["", "nan"]:
            continue

        result.append({
            "row_excel": i + header_row + 2,
            "ten_goc": ten_goc,
            "ten_chuan": ten_chuan,
        })

    return result