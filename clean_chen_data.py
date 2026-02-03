import pandas as pd
import re

def normalize_date(date_str):
    if pd.isna(date_str) or str(date_str).strip() in ["", "nan"]: return ""
    
    # 1. 轉成字串並清理前後空格與單引號
    d = str(date_str).strip().replace("'", "")
    
    # 2. 【核心修正】：移除 Excel 自動產生的 00:00:00 時間尾巴
    # 我們只取空格前的前半段 (日期部分)
    if " " in d:
        d = d.split(" ")[0]
        
    return d

def process_inventory(file_path):
    # 讀取 Excel
    print(f"正在讀取 {file_path}...")
    df_raw = pd.read_excel(file_path, header=None, engine='openpyxl')
    all_rows = []
    
    for i in range(0, len(df_raw), 12):
        header_label = str(df_raw.iloc[i, 0])
        tag_match = re.match(r'(\d+)-(\d+)-(.*)', header_label)
        if not tag_match: continue
        
        rack, box, owner = tag_match.groups()
        box_name = f"{box}_{owner}"

        # 暫存這個盒子的所有資料以計算空位
        box_data = []
        for row_offset in range(10):
            current_row = i + 2 + row_offset
            for col_idx in range(1, 11):
                cell_name_col = (col_idx * 2) - 1
                date_col = (col_idx * 2)
                
                cell_name = str(df_raw.iloc[current_row, cell_name_col]).strip()
                cell_name = "" if cell_name in ["nan", ""] else cell_name
                freeze_date = normalize_date(df_raw.iloc[current_row, date_col])
                
                status = 1 if cell_name != "" else 0
                pos = (row_offset * 10) + col_idx
                
                # 【新增欄位】：Unique_ID (格式: R1-B4_聖萍-1)
                unique_id = f"R{rack}-B{box_name}-{pos}"
                
                # 【移除欄位】：不再加入 Tank 欄位
                box_data.append({
                    "Unique_ID": unique_id,
                    "Rack": rack, 
                    "Box": box_name,
                    "Position": pos, 
                    "Cell_Name": cell_name, 
                    "Freeze_Date": freeze_date, 
                    "Status": status
                })
        
        # 計算空位
        occupied_count = sum(d['Status'] for d in box_data)
        empty_slots = 100 - occupied_count
        
        for d in box_data:
            d['Empty_Slots'] = empty_slots
            all_rows.append(d)
                
    return pd.DataFrame(all_rows)

# 執行並儲存
final_df = process_inventory("chen-lab-cell-inventory-20240926.xlsx")
final_df.to_csv("cleaned_chen_lab.csv", index=False, encoding="utf-8-sig")
print("✨ v2 版本清洗完成！已移除 Tank 並新增 Unique_ID 與日期修正。")