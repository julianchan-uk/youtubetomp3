import streamlit as st
import yt_dlp
import os

st.set_page_config(page_title="YouTube 下載器", page_icon="🎥")
st.title("🎥 YouTube 影片下載工具")

# 這裡加入簡單的說明
st.info("請在下方輸入 YouTube 網址，系統會嘗試解析並提供下載按鈕。")

url = st.text_input("請貼上 YouTube 影片網址:")

if url:
    try:
        # 下載設定
        save_path = "video.mp4"
        ydl_opts = {
            'format': 'best', 
            'outtmpl': save_path,
        }

        with st.spinner('正在處理影片，請稍候...'):
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # 提取資訊並下載到伺服器暫存
                info = ydl.extract_info(url, download=True)
                video_title = info.get('title', 'video')

        # 讀取暫存檔並顯示下載按鈕
        if os.path.exists(save_path):
            with open(save_path, "rb") as f:
                st.success(f"✅ 已成功解析：{video_title}")
                st.download_button(
                    label="📥 點擊這裡下載影片到你的裝置",
                    data=f,
                    file_name=f"{video_title}.mp4",
                    mime="video/mp4"
                )
            # 刪除伺服器上的暫存檔
            os.remove(save_path)

    except Exception as e:
        st.error(f"出錯了：{e}")
        st.warning("提示：如果出現 403 錯誤，通常是 YouTube 暫時封鎖了伺服器的 IP，請稍後再試。")
