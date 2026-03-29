import streamlit as st
import requests

st.set_page_config(page_title="私人 OMV 下載器", page_icon="🎬")
st.title("🎬 YouTube 高清下載 (OMV 專線)")

# --- 設定你的 DDNS 地址 ---
# 注意：確保路由器已轉發 8888 端口到 192.168.1.101
API_URL = "http://Chanwaiman.ddns.net:8124/download"

url = st.text_input("📌 貼上 YouTube 影片網址：", placeholder="https://www.youtube.com/watch?v=...")

if url:
    if st.button("🚀 開始解析並從家裡下載"):
        try:
            with st.spinner("正在聯絡家中的 OMV 進行下載..."):
                # 發送請求到 DDNS
                response = requests.get(API_URL, params={'url': url}, timeout=600)
                
                if response.status_code == 200:
                    st.success("✅ 下載成功！")
                    st.download_button(
                        label="📥 儲存影片到電腦",
                        data=response.content,
                        file_name="video.mp4",
                        mime="video/mp4",
                        use_container_width=True
                    )
                else:
                    st.error(f"❌ 伺服器錯誤: {response.text}")
                    
        except Exception as e:
            st.error(f"❌ 無法連線至 Chanwaiman.ddns.net")
            st.info("💡 檢查清單：\n1. 路由器 Port 8888 是否已開放？\n2. OMV 上的 Docker 是否顯示為綠色 Up？")
