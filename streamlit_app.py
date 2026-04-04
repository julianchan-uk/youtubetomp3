import streamlit as st
import requests

st.set_page_config(page_title="私人 OMV 下載器", page_icon="🎬")
st.title("🎬 YouTube 高清下載 (OMV 專線)")

# --- 設定你的 DDNS 地址 ---
API_URL = "http://Chanwaiman.ddns.net:8888/download"

url = st.text_input("📌 貼上 YouTube 影片網址：", placeholder="https://www.youtube.com/watch?v=...")

# 新增格式選擇，與您的 main.py 對齊
download_format = st.selectbox("選擇格式：", ["1080p MP4", "720p MP4", "320k MP3", "192k MP3"])

if url:
    if st.button("🚀 開始解析並從家裡下載"):
        try:
            with st.spinner("正在聯絡家中的 OMV 進行下載..."):
                # --- 關鍵修正 1：將格式名稱轉為 API 識別的字串 ---
                fmt_map = {
                    "1080p MP4": "1080p",
                    "720p MP4": "low",
                    "320k MP3": "320k",
                    "192k MP3": "192k"
                }
                
                # --- 關鍵修正 2：改用 requests.post 並發送 json ---
                payload = {
                    "url": url,
                    "format": fmt_map.get(download_format, "1080p")
                }
                
                # 注意：因影片下載較久，timeout 建議設長一點
                response = requests.post(API_URL, json=payload, timeout=900)
                
                if response.status_code == 200:
                    st.success("✅ 下載成功！")
                    
                    # 嘗試從 Header 獲取檔名（選配）
                    content_disp = response.headers.get("Content-Disposition", "")
                    default_name = "video.mp4" if "MP4" in download_format else "music.mp3"
                    
                    st.download_button(
                        label="📥 儲存到電腦",
                        data=response.content,
                        file_name=default_name,
                        mime="video/mp4" if "MP4" in download_format else "audio/mpeg",
                        use_container_width=True
                    )
                else:
                    st.error(f"❌ 伺服器錯誤: {response.text}")
                    
        except Exception as e:
            st.error(f"❌ 無法連線至 Chanwaiman.ddns.net")
            st.info(f"💡 偵錯資訊: {str(e)}")
            
