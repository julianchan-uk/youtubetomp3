import streamlit as st
import requests

st.set_page_config(page_title="私人 YouTube 下載器", page_icon="🏠")
st.title("🎬 私人 YouTube 高清下載 (透過 OMV)")

# 使用你的 DDNS 地址
OMV_API_URL = "http://Chanwaiman.ddns.net:8888/download" 

url = st.text_input("📌 請貼上 YouTube 網址：")

if url and st.button("🚀 開始下載"):
    try:
        with st.spinner("正在叫家裡的 OMV 抓片中..."):
            # 發送請求到你的 DDNS
            response = requests.get(OMV_API_URL, params={'url': url}, timeout=600)
            
            if response.status_code == 200:
                st.success("✅ 下載完成！")
                st.download_button(
                    label="📥 儲存影片到電腦",
                    data=response.content,
                    file_name="video.mp4",
                    mime="video/mp4"
                )
            else:
                st.error(f"❌ OMV 錯誤: {response.text}")
    except Exception as e:
        st.error(f"❌ 連不到家裡的伺服器: {e}")
        st.info("請檢查路由器 Port 8888 是否已開放，以及 DDNS 是否指向正確 IP。")
