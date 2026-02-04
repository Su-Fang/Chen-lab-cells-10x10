🧬 陳教授 10x10 大型液態氮庫存管理系統

這是一個專為實驗室開發的智慧化液態氮庫存管理系統。
針對傳統 Excel 紀錄難以與實體位置對應的痛點，本系統提供直觀的 10x10 空間網格視覺化與快速檢索功能，大幅提升細胞找尋與存放的效率。

🚀 核心功能 (Key Features)
1. 🔍 智慧快速檢索–全域搜尋：支援模糊搜尋，輸入細胞名稱即可跨 Rack/Box 鎖定位置。🌎 即時定位：直接顯示目標細胞的鐵架編號、盒子編號與座標。

2. 🧊 10x10 視覺化地圖：實體模擬：完美呈現 10x10 冷凍盒配置，綠色代表已佔用，灰色代表空位。智慧處理長字串，確保在手機或電腦上查看時網格皆整齊不變形。

3. 📊 庫存動態儀表板：自動統計：即時計算全室 4,000 管細胞的使用率與剩餘空間。空位排行榜：自動推薦空位最多的盒子，導引使用者進行空間優化。

4. 🖨️ 專業標籤列印模式
黑字清晰化：專為列印設計的 CSS，將文字強制轉為純黑色，確保標籤易於讀取。
隱身導航：列印時自動隱藏操作按鈕，僅保留核心網格。

🛠️ 技術細節 (Tech Stack)
Frontend: Streamlit (Python-based web framework)
Data Source: Google Sheets API (CSV export)
Styling: Custom CSS injection for print optimization & UI enhancement

Deployment: Streamlit Cloud

🖨️ 列印操作指引 (Printing Instructions)
為了產出最適合貼在液態氮桶旁的 「一頁 A4 標籤報表」，請依照以下步驟設定：
點擊側邊欄的 「啟動列印模式」。
使用瀏覽器列印功能 (Cmd+P 或 Ctrl+P)。

關鍵設定值：
方向 (Layout)：直向 (Portrait)
縮放 (Scale)：50%

Note: 列印完成後，點擊頁面頂端的「⬅️ 結束列印」按鈕，即可完美彈回網頁模式。

🤝 系統開發: Gemini + Su-Fnag 🌷
