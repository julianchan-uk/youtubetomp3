import streamlit as st
import yt_dlp
import os

st.set_page_config(page_title="YouTube 下載器", page_icon="🎥")
st.title("🎥 YouTube 影片下載工具")

url = st.text_input("請貼上 YouTube 影片網址:")

if url:
    try:
        # 設定下載選項
        ydl_opts = {
            'format': 'best', # 下載最高品質（含影音）
            'outtmpl': 'downloaded_video.mp4',
        }

        with st.spinner('正在解析影片資訊...'):
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                title = info.get('title', 'video')
                
        # 讀取檔案並提供下載按鈕
        with open("downloaded_video.mp4", "rb") as file:
            st.video(file) # 在網頁預覽
            st.download_button(
                label="📥 點擊下載影片到電腦",
                data=file,
                file_name=f"{title}.mp4",
                mime="video/mp4"
            )
        
        # 清理伺服器空間
        os.remove("downloaded_video.mp4")

    except Exception as e:
        st.error(f"發生錯誤: {e}")
        st.info("提示：如果出現 403 錯誤，通常是 YouTube 封鎖了伺服器的 IP。")
