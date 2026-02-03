import streamlit as st
import pandas as pd

# 1. 基礎設定：強制寬版顯示
st.set_page_config(layout="wide", page_title="陳教授 10x10 大型液態氮系統")

# 2. 定義逃生艙功能 (必須放在最前面以重置狀態)
if 'print_key' not in st.session_state:
    st.session_state['print_key'] = False

def deactivate_print_mode():
    st.session_state["print_key"] = False

# 3. 定義全域 CSS (處理表格黑大粗與數據卡片大小)
def inject_global_css():
    st.markdown("""
        <style>
        /* 數值卡片縮小 (例如 4000, 1658) */
        [data-testid="stMetricValue"] { font-size: 28px !important; }
        [data-testid="stMetricLabel"] { font-size: 16px !important; }
        
        /* 標題與表格優化 (黑大粗) */
        h3 { font-size: 20px !important; }
        [data-testid="stTable"] td, [data-testid="stTable"] th {
            text-align: center !important;
            font-weight: 700 !important;
            color: black !important;
            font-size: 22px !important;
            padding: 10px !important;
        }
        /* 隱藏表格第一欄序號 */
        div[data-testid="stTable"] th:first-child, 
        div[data-testid="stTable"] td:first-child { display: none !important; }
        </style>
    """, unsafe_allow_html=True)

inject_global_css()

# --- 側邊欄：模式切換 ---
st.sidebar.title("🛠️ 系統選單")
print_mode = st.sidebar.checkbox("🖨️ 啟動列印模式 (適合列印單一盒子)", key="print_key")

# --- 讀取資料 ---
sheet_url = "https://docs.google.com/spreadsheets/d/1YtJ8HNQxDxNj_n27984Nf_RV3yxVBojK7WoubhXqLqM/export?format=csv"
df = pd.read_csv(sheet_url)

# --- 標題區 ---
st.title("🧬 陳教授 10x10 大型液態氮桶")

if print_mode:
    # --- 🖨️ 列印模式專屬邏輯 ---
    st.markdown('<div class="no-print">', unsafe_allow_html=True)
    # st.warning("⚠️ 目前處於【列印模式】，側邊欄已隱藏。")
    if st.button("⬅️ 結束列印並返回網頁模式", on_click=deactivate_print_mode):
        st.rerun()
    # st.info("💡 提示：請按 Command+P，設定 Portrait (直向) 且縮放為 50% 以獲得最佳效果。")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 注入「列印模式」專用 CSS
    st.markdown("""
        <style>
        /* 1. 隱藏不必要元素 */
        [data-testid="stSidebar"], header, footer { display: none !important; }
        
        /* 2. 在列印時隱藏警告提示與按鈕 */
        @media print {
            .no-print, button { display: none !important; }
            .stAlert, .stAlert p, .stAlert b { color: black !important; } /* 強制黑字 */
            body { -webkit-print-color-adjust: exact !important; }
        }

        /* 3. 網格微調 (配合手動 50% 縮放) */
        .main .block-container { padding: 0.5rem !important; }
        [data-testid="column"] { padding: 1px !important; margin: 0px !important; }
        .stAlert { padding: 2px !important; margin-bottom: 2px !important; min-height: 50px !important; }
        .stAlert p, .stAlert b { font-size: 10pt !important; line-height: 1.1 !important; color: black !important; }
        </style>
    """, unsafe_allow_html=True)


# --- 側邊欄：操作說明 ---
with st.sidebar.expander("📖 系統使用操作說明", expanded=False):
    st.markdown("""
    ### 1. 🔍 快速檢索
    * 在上方輸入**細胞名稱**關鍵字，系統會列出所有相符的細胞及其所在的「鐵架、盒子、編號」。
    * 支援模糊搜尋（例如輸入 `HEp2` 即可找到所有相關編號）。

    ### 2. 📦 空間視覺化
    * 選擇「鐵架」與「盒子」後，下方會出現 **10x10 網格圖**。
    * **綠色格子**：代表已有存放細胞。
    * **灰色格子**：代表該位置為空位。

    ### 3. 📊 庫存管理
    * **庫存概況**：即時計算全實驗室的容量與使用率。
    * **空位排行榜**：系統會自動推薦目前「最空」的盒子，建議優先存放在這些位置以節省空間。

    ### 4. 🖨️ 列印標籤圖 (重要!)
    若要印出紙本貼在液態氮桶旁：
    1. 勾選「**啟動列印模式**」。
    2. 按下鍵盤 **Command + P** (Mac) 或 **Ctrl + P** (Windows)。
    3. **列印設定務必選擇：**
        * **方向**：直向 (Portrait)
        * **縮放 (Scale)**：手動輸入 **50%**
        * **背景圖形**：務必「打勾」(顏色才印得出來)
    4. 印完後點擊「⬅️ 結束列印」返回。
    """)


# --- 側邊欄其餘內容 ---
st.sidebar.divider()
st.sidebar.header("🔍 快速檢索")
search_query = st.sidebar.text_input("輸入細胞名稱搜尋...", "")
selected_rack = st.sidebar.selectbox("選擇鐵架 (Rack)", sorted(df['Rack'].unique()))
boxes_in_rack = sorted(df[df['Rack'] == selected_rack]['Box'].unique())
selected_box = st.sidebar.selectbox("選擇盒子 (Box)", boxes_in_rack)

# --- 儀表板區塊 (列印模式下隱藏) ---
if not print_mode:
    st.markdown("### 📊 庫存概況")
    total_capacity = len(df)
    total_occupied = df[df['Status'] == 1].shape[0]
    total_empty = total_capacity - total_occupied
    occupancy_rate = (total_occupied / total_capacity) * 100

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("總容量", f"{total_capacity} 管")
    m2.metric("已使用", f"{total_occupied} 管")
    m3.metric("剩餘空位", f"{total_empty} 管")
    m4.metric("使用率", f"{occupancy_rate:.1f} %")
    st.divider()

# --- 主畫面：10x10 網格 ---
if search_query:
    search_results = df[df['Cell_Name'].str.contains(search_query, case=False, na=False)]
    st.subheader(f"🔎 搜尋結果 ({len(search_results)} 筆)")
    st.table(search_results[['Rack', 'Box', 'Position', 'Cell_Name', 'Freeze_Date']])
else:
    box_data = df[(df['Rack'] == selected_rack) & (df['Box'] == selected_box)].sort_values('Position')
    empty_val = box_data['Empty_Slots'].iloc[0]
    
    st.subheader(f"📦 Rack {selected_rack} - Box {selected_box} (剩餘空位: {empty_val} / 100)")

    # 繪製 10x10 網格
    for row in range(10):
        cols = st.columns(10)
        for col in range(10):
            pos = row * 10 + col + 1
            cell_info = box_data[box_data['Position'] == pos].iloc[0]
            
            # 12 個字自動截斷，維持高度一致
            d_name = str(cell_info['Cell_Name'])
            if len(d_name) > 12:
                d_name = d_name[:10] + ".."
                
            with cols[col]:
                if cell_info['Status'] == 1:
                    st.success(f"**{pos}**\n{d_name}\n{cell_info['Freeze_Date']}")
                else:
                    st.info(f"**{pos}**\n(Empty)")

# --- 空位排行榜 (列印模式下隱藏) ---
if not print_mode:
    st.divider()
    st.subheader("📊 鐵架空位統計 (建議優先存放)")
    summary = df.groupby(['Rack', 'Box'])['Empty_Slots'].first().reset_index()
    top_empty = summary.sort_values('Empty_Slots', ascending=False).head(5)
    top_empty.columns = ['鐵架', '盒子', '目前空位數']
    st.table(top_empty)