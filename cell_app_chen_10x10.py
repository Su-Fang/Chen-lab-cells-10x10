import streamlit as st
import pandas as pd

# 1. 基礎設定
st.set_page_config(layout="wide", page_title="陳教授 10x10 大型液態氮系統")

# 2. 逃生艙按鈕狀態設定
if 'print_key' not in st.session_state:
    st.session_state['print_key'] = False

def deactivate_print_mode():
    st.session_state["print_key"] = False

# 3. 全域 CSS 優化
def inject_global_css():
    st.markdown("""
        <style>
        [data-testid="stMetricValue"] { font-size: 28px !important; }
        [data-testid="stMetricLabel"] { font-size: 16px !important; }
        h3 { font-size: 20px !important; }
        [data-testid="stTable"] td, [data-testid="stTable"] th {
            text-align: center !important;
            font-weight: 700 !important;
            color: black !important;
            font-size: 20px !important;
            padding: 10px !important;
        }
        div[data-testid="stTable"] th:first-child, 
        div[data-testid="stTable"] td:first-child { display: none !important; }
        </style>
    """, unsafe_allow_html=True)

inject_global_css()

# 4. 讀取資料 (改為直接讀取，移除快取以減少網頁閃爍)
sheet_url = "https://docs.google.com/spreadsheets/d/1YtJ8HNQxDxNj_n27984Nf_RV3yxVBojK7WoubhXqLqM/export?format=csv"
df = pd.read_csv(sheet_url)

# --- 側邊欄：控制台 ---
st.sidebar.title("🛠️ 系統選單")
print_mode = st.sidebar.checkbox("🖨️ 啟動列印模式", key="print_key")

with st.sidebar.expander("📖 系統使用操作說明", expanded=False):
    st.markdown("""
    ### 1. 💾 資料更新規範 (重要)
    * **入庫**：請在試算表中填入細胞名稱，並將 **Status 設為 1**。
    * **出庫**：請刪除細胞名稱，並將 **Status 設為 0**。
    * **自動計算**：App 會自動計算空位，不需手動填寫 Empty_Slots。

    ### 2. 🔍 快速檢索
    * 輸入名稱關鍵字即可跨盒搜尋。

    ### 3. 🖨️ 列印設定
    * 開啟列印模式後，按 **Cmd/Ctrl + P**。
    * 設為 **Portrait (直向)**、**Scale 50%** 並勾選 **背景圖形**。
    """)

st.sidebar.divider()
search_query = st.sidebar.text_input("🔍 輸入細胞名稱搜尋...", "")
selected_rack = st.sidebar.selectbox("選擇鐵架 (Rack)", sorted(df['Rack'].unique()))
boxes_in_rack = sorted(df[df['Rack'] == selected_rack]['Box'].unique())
selected_box = st.sidebar.selectbox("選擇盒子 (Box)", boxes_in_rack)

st.sidebar.divider()
st.sidebar.link_button("🔗 開啟 Google Sheets 原始表單", "https://docs.google.com/spreadsheets/d/1YtJ8HNQxDxNj_n27984Nf_RV3yxVBojK7WoubhXqLqM/edit")

# --- 主畫面邏輯 ---
st.title("🧬 陳教授 10x10 大型液態氮桶")

if print_mode:
    # 列印模式導航
    st.markdown('<div class="no-print">', unsafe_allow_html=True)
    if st.button("⬅️ 結束列印並返回網頁模式", on_click=deactivate_print_mode):
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 列印模式專用 CSS
    st.markdown("""
        <style>
        [data-testid="stSidebar"], header, footer { display: none !important; }
        @media print {
            .no-print, button { display: none !important; }
            .stAlert, .stAlert p, .stAlert b { color: black !important; } 
            body { -webkit-print-color-adjust: exact !important; }
        }
        .main .block-container { padding: 0.5rem !important; }
        [data-testid="column"] { padding: 1px !important; margin: 0px !important; }
        .stAlert { padding: 2px !important; margin-bottom: 2px !important; min-height: 50px !important; }
        .stAlert p, .stAlert b { font-size: 10pt !important; line-height: 1.1 !important; color: black !important; }
        </style>
    """, unsafe_allow_html=True)

# 數據計算
total_capacity = len(df)
total_occupied = (df['Status'] == 1).sum()
total_empty = total_capacity - total_occupied

# 顯示儀表板 (列印模式下隱藏)
if not print_mode:
    st.markdown("### 📊 庫存概況")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("總容量", f"{total_capacity} 管")
    m2.metric("已使用", f"{total_occupied} 管")
    m3.metric("剩餘空位", f"{total_empty} 管")
    m4.metric("使用率", f"{(total_occupied/total_capacity)*100:.1f} %")
    st.divider()

# 顯示搜尋結果或 10x10 網格
if search_query:
    search_results = df[df['Cell_Name'].str.contains(search_query, case=False, na=False)]
    st.subheader(f"🔎 搜尋結果 ({len(search_results)} 筆)")
    st.table(search_results[['Rack', 'Box', 'Position', 'Cell_Name', 'Freeze_Date']])
else:
    box_data = df[(df['Rack'] == selected_rack) & (df['Box'] == selected_box)].sort_values('Position')
    # 自動計算該盒空位
    box_empty_count = (box_data['Status'] == 0).sum()
    st.subheader(f"📦 Rack {selected_rack} - Box {selected_box} (即時空位: {box_empty_count}/100)")

    for row in range(10):
        cols = st.columns(10)
        for col in range(10):
            pos = row * 10 + col + 1
            cell_info = box_data[box_data['Position'] == pos].iloc[0]
            d_name = str(cell_info['Cell_Name'])
            if len(d_name) > 12: d_name = d_name[:10] + ".."
            
            with cols[col]:
                if cell_info['Status'] == 1:
                    st.success(f"**{pos}**\n{d_name}\n{cell_info['Freeze_Date']}")
                else:
                    st.info(f"**{pos}**\n(Empty)")

# 空位排行榜 (即時計算)
if not print_mode:
    st.divider()
    st.subheader("📊 鐵架空位統計 (建議優先存放)")
    # 使用程式即時計算每個盒子的空位數
    rank_df = df[df['Status'] == 0].groupby(['Rack', 'Box']).size().reset_index(name='Empty_Count')
    top_empty = rank_df.sort_values('Empty_Count', ascending=False).head(5)
    top_empty.columns = ['鐵架', '盒子', '目前空位數']
    st.table(top_empty)