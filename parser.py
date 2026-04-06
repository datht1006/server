import pandas as pd

def parse_2_columns(file_obj):
    raw = pd.read_excel(file_obj, header=None)

    # Tìm header row
    header_row = None
    for i in range(20):
        row = raw.iloc[i].astype(str).str.lower()
        if row.str.contains("tên gọi vật tư").any():
            header_row = i
            break

    if header_row is None:
        raise ValueError("Không tìm thấy header")

    # Đọc lại với header đúng
    df = pd.read_excel(file_obj, header=header_row)
    df.columns = df.columns.astype(str).str.strip().str.lower()

    # ===== MAP CỘT =====
    # key = tên field trả về, value = list các từ khóa để tìm trong header
    COLUMN_MAP = {
        "chi_tieu":              ["chỉ tiêu"],
        "bp_phu_trach":          ["bp phụ trách"],
        "nhom_vat_tu":           ["nhóm vật tư"],
        "ma_vat_tu":             ["mã vật tư"],
        "ma_vat_tu_bosco":       ["mã vật tư trên bosco"],
        "ngach":                 ["ngạch"],
        "ferro_bv":              ["ferro"],
        "hoa_phat_dong":         ["hòa phát đông"],
        "cum":                   ["cụm"],
        "kho":                   ["kho"],
        "nam_hop":               ["năm hợp"],
        "ten_goi_vat_tu":        ["tên gọi vật tư"],
        "ten_vat_tu_chuan":      ["tên vật tư chuẩn không giới hạn"],
        "don_vi_tinh":           ["đơn vị tính"],
        "don_vi_tinh_hieu_luc":  ["đơn vị tính hiệu lực"],
        "kich_hoat_dvt":         ["kích hoạt dvt"],
        "dvt_dich_vu_song_song": ["dịch vụ song song"],
        "don_trung":             ["đơn trung"],
        "ma_loai":               ["mã loại"],
        "ma_tot_loai_bong":      ["loại bóng chuẩn hóa"],
        "ma_tot_dich_vu":        ["loại bóng dịch vụ"],
        "nguon_ton_kho":         ["nguồn tồn kho"],
        "pham_vi_ton_kho":       ["phạm vi tồn kho"],
        "dong_co":               ["đồng cơ", "động cơ"],
        "hang_san_xuat":         ["hãng sản xuất"],
        "ma_ih":                 ["mã ih"],
        "quoc_gia":              ["quốc gia"],
        "phan_cap_l1":           ["phân cấp l1"],
        "phan_cap_l2":           ["phân cấp l2"],
        "phan_cap_l3":           ["phân cấp l3"],
        "phe_thay":              ["phê thay"],
        "mat_thay":              ["mắt thay"],
        "loai_chat_luong":       ["loại chất lượng"],
        "so_cay_so":             ["số cấy sô", "số cây số"],
        "quy_cach":              ["quy cách"],
        "tieu_chuan_chat_luong": ["tiêu chuẩn chất lượng"],
        "phuong_thuc_luu_kho":   ["phương thức lưu kho"],
        "ghi_chu":               ["ghi chú"],
    }

    # Tự động map tên cột thực tế trong file
    col_map_actual = {}
    for field, keywords in COLUMN_MAP.items():
        for col in df.columns:
            if any(kw in col for kw in keywords):
                col_map_actual[field] = col
                break  # lấy cột đầu tiên khớp

    # Cột bắt buộc để lọc dòng trống
    col_ten_goi = col_map_actual.get("ten_goi_vat_tu")
    if not col_ten_goi:
        raise ValueError("Không tìm thấy cột 'Tên gọi vật tư'")

    result = []

    for i, row in df.iterrows():
        ten_goi = str(row[col_ten_goi]).strip()
        if ten_goi.lower() in ["", "nan"]:
            continue

        record = {"row_excel": i + header_row + 2}

        for field, actual_col in col_map_actual.items():
            val = row.get(actual_col, "")
            val = str(val).strip()
            # Bỏ giá trị "nan"
            record[field] = "" if val.lower() == "nan" else val

        result.append(record)

    return result