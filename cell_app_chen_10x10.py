import streamlit as st
import pandas as pd

# 1. 基礎設定
st.set_page_config(layout="wide", page_title="陳教授 10x10 大型液態氮系統")

# 2. 狀態管理 (解決返回報錯問題)
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
            font-size: 18px !important;
            padding: 8px !important;
        }
        div[data-testid="stTable"] th:first-child, 
        div[data-testid="stTable"] td:first-child { display: none !important; }
        
        /* 10x10 網格文字大小調整 */
        .stAlert p, .stAlert b { font-size: 10pt !important; line-height: 1.1 !important; }
        </style>
    """, unsafe_allow_html=True)

inject_global_css()

# 4. 讀取資料 (維持陳老師的試算表連結)
sheet_url = "https://docs.google.com/spreadsheets/d/1YtJ8HNQxDxNj_n27984Nf_RV3yxVBojK7WoubhXqLqM/export?format=csv"
df = pd.read_csv(sheet_url)

# --- ✨ 核心升級：全自動感應邏輯 ---
def calculate_status(row):
    name = str(row['Cell_Name']).strip().lower()
    # 判定「空位」：nan, 空白, 或是各種橫線符號
    if not name or name in ['nan', '', '-', '–', 'none']:
        return 0
    return 1

df['Effective_Status'] = df.apply(calculate_status, axis=1)
# -----------------------------------------------

# --- 側邊欄：控制台 ---
st.sidebar.title("🛠️ 系統選單")
print_mode = st.sidebar.checkbox("🖨️ 啟動列印模式", key="print_key")

with st.sidebar.expander("📖 系統使用操作說明", expanded=False):
    st.markdown("""
    ### 🔬 數據維護規範
    * **入庫**：填寫名稱並手動將 **Status 設為 1**。
    * **出庫**：清空名稱並手動將 **Status 設為 0**。
    
    ### 🛡️ 智慧感應機制
    * 本系統配備自動判定：**以細胞名稱為準**。
    * 刪除名稱後，地圖會自動恢復灰色空位，確保統計精確。
    """)

st.sidebar.divider()
search_query = st.sidebar.text_input("🔍 輸入細胞名稱搜尋...", "")
selected_rack = st.sidebar.selectbox("選擇鐵架 (Rack)", sorted(df['Rack'].unique()))
boxes_in_rack = sorted(df[df['Rack'] == selected_rack]['Box'].unique())
selected_box = st.sidebar.selectbox("選擇盒子 (Box)", boxes_in_rack)

st.sidebar.divider()
st.sidebar.link_button("🔗 開啟 Google Sheets 原始表單", "https://docs.google.com/spreadsheets/d/1YtJ8HNQxDxNj_n27984Nf_RV3yxVBojK7WoubhXqLqM/edit")

# --- 🖨️ 列印模式：隱身術與黑白修正 ---
if print_mode:
    if st.button("⬅️ 結束列印並返回", on_click=deactivate_print_mode):
        st.rerun()
    
    st.markdown('<p class="no-print" style="color:red; font-weight:bold;">列印預覽：側邊欄已隱藏，按 Ctrl/Cmd + P 列印</p>', unsafe_allow_html=True)

    st.markdown("""
        <style>
        /* 網頁顯示時隱藏側邊欄 */
        section[data-testid="stSidebar"], 
        [data-testid="stSidebarCollapsedControl"],
        header, footer { display: none !important; }

        @media print {
            .no-print, button, .stButton { display: none !important; }
            
            /* 【核心修正】保留背景顏色，但文字變黑 */
            .stAlert {
                /* 強制瀏覽器印出背景顏色 */
                -webkit-print-color-adjust: exact !important;
                print-color-adjust: exact !important;
                color: black !important;
                border: 1px solid #ccc !important; /* 加個淡淡的框線更有質感 */
            }
            
            /* 強制框框內所有文字（含加粗）為黑色 */
            .stAlert p, .stAlert b, .stAlert div, .stAlert span {
                color: black !important;
                -webkit-text-fill-color: black !important;
            }
                
            .stAlert svg { display: none !important; } /* 隱藏圖示 */
            
            body { -webkit-print-color-adjust: economy !important; }
        }
        .main .block-container { padding-top: 1rem !important; max-width: 100% !important; }
        </style>
    """, unsafe_allow_html=True)

# 數據計算 (改用 Effective_Status)
total_capacity = len(df)
total_occupied = (df['Effective_Status'] == 1).sum()
total_empty = total_capacity - total_occupied

# 顯示儀表板 (列印模式下隱藏)
if not print_mode:
    st.markdown("### 📊 全庫庫存概況")
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
    # 即時計算該盒空位
    box_empty_count = (box_data['Effective_Status'] == 0).sum()
    st.subheader(f"📦 Rack {selected_rack} - Box {selected_box} (空位: {box_empty_count}/100)")

    for row in range(10):
        cols = st.columns(10)
        for col in range(10):
            pos = row * 10 + col + 1
            cell_info = box_data[box_data['Position'] == pos].iloc[0]
            d_name = str(cell_info['Cell_Name'])
            if len(d_name) > 12: d_name = d_name[:10] + ".."
            
            with cols[col]:
                if cell_info['Effective_Status'] == 1:
                    st.success(f"**{pos}**\n{d_name}\n{cell_info['Freeze_Date']}")
                else:
                    st.info(f"**{pos}**\n(Empty)")

# 空位排行榜 (即時計算)
if not print_mode:
    st.divider()
    st.subheader("📊 鐵架空位排行榜")
    rank_df = df[df['Effective_Status'] == 0].groupby(['Rack', 'Box']).size().reset_index(name='Empty_Count')
    top_empty = rank_df.sort_values('Empty_Count', ascending=False).head(5)
    top_empty.columns = ['鐵架', '盒子', '目前空位']
    st.table(top_empty)