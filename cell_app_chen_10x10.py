import streamlit as st
import pandas as pd

# 設定網頁寬度為最大，方便顯示 10 欄
st.set_page_config(layout="wide", page_title="陳教授 10x10 大型液態氮系統")

def inject_custom_css():
    st.markdown("""
        <style>
        /* 讓 10x10 網格更緊湊，字體縮小至 12px */
        .stAlert { padding: 5px !important; margin-bottom: 5px !important; }
        .cell-box { 
            font-size: 12px !important; 
            line-height: 1.2; 
            height: 60px; 
            overflow: hidden;
            border: 1px solid #ddd;
            border-radius: 4px;
            padding: 2px;
            text-align: center;
        }
        /* 表格置中黑大粗 (沿用您的最愛) */
        .stTable td, .stTable th { 
            text-align: center !important; 
            font-weight: 700 !important; 
            color: black !important;
            font-size: 18px !important;
        }
        div[data-testid="stTable"] th:first-child, 
        div[data-testid="stTable"] td:first-child { display: none !important; }
        </style>
    """, unsafe_allow_html=True)

inject_custom_css()

st.title("🧬 陳教授 10x10 巨型液態氮桶")

# 讀取您剛產出的 CSV
sheet_url = "https://docs.google.com/spreadsheets/d/1YtJ8HNQxDxNj_n27984Nf_RV3yxVBojK7WoubhXqLqM/export?format=csv"
# 轉換成可瀏覽的網址
display_url = sheet_url.replace("/export?format=csv", "")

# 讀取資料
df = pd.read_csv(sheet_url)


# --- 側邊欄控制 ---
# 2. 側邊欄：加入即時來源連結
st.sidebar.markdown(f"📊 **即時數據來源：**\n[Google Sheets 雲端主表]({display_url})")
st.sidebar.divider()

# ... 側邊欄搜尋邏輯 ...

# 3. 庫存概況區塊 (放在標題下方)
st.markdown("### 📊 庫存概況")
total_capacity = len(df)
total_occupied = df[df['Status'] == 1].shape[0]
total_empty = total_capacity - total_occupied
occupancy_rate = (total_occupied / total_capacity) * 100

# 使用大數字組件顯示
m1, m2, m3, m4 = st.columns(4)
m1.metric("總容量", f"{total_capacity} 管")
m2.metric("已使用", f"{total_occupied} 管")
m3.metric("剩餘空位", f"{total_empty} 管")
m4.metric("使用率", f"{occupancy_rate:.1f} %")

st.divider()

st.sidebar.header("🔍 快速檢索")
search_query = st.sidebar.text_input("輸入細胞名稱搜尋...", "")
selected_rack = st.sidebar.selectbox("選擇鐵架 (Rack)", sorted(df['Rack'].unique()))
boxes_in_rack = sorted(df[df['Rack'] == selected_rack]['Box'].unique())
selected_box = st.sidebar.selectbox("選擇盒子 (Box)", boxes_in_rack)

# --- 邏輯處理 ---
if search_query:
    # 搜尋模式
    search_results = df[df['Cell_Name'].str.contains(search_query, case=False, na=False)]
    st.subheader(f"🔎 搜尋結果 ({len(search_results)} 筆)")
    st.table(search_results[['Rack', 'Box', 'Position', 'Cell_Name', 'Freeze_Date']])
else:
    # 儀表板模式
    box_data = df[(df['Rack'] == selected_rack) & (df['Box'] == selected_box)].sort_values('Position')
    empty_val = box_data['Empty_Slots'].iloc[0]
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.subheader(f"📦 Rack {selected_rack} - Box {selected_box}")
    with col2:
        st.metric("剩餘空位", f"{empty_val} / 100")

    # 繪製 10x10 網格
    for row in range(10):
        cols = st.columns(10)
        for col in range(10):
            pos = row * 10 + col + 1
            cell_info = box_data[box_data['Position'] == pos].iloc[0]
            
            with cols[col]:
                if cell_info['Status'] == 1:
                    # 有細胞：綠色
                    st.success(f"**{pos}**\n{cell_info['Cell_Name']}\n{cell_info['Freeze_Date']}")
                else:
                    # 空位：灰色
                    st.info(f"**{pos}**\n(Empty)")

# --- 空位排行榜 ---
st.divider()
st.subheader("📊 鐵架空位統計 (建議優先存放)")
summary = df.groupby(['Rack', 'Box'])['Empty_Slots'].first().reset_index()
top_empty = summary.sort_values('Empty_Slots', ascending=False).head(5)
top_empty.columns = ['鐵架', '盒子', '目前空位數']
st.table(top_empty)