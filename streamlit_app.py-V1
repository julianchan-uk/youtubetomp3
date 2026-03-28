import streamlit as st
import yt_dlp
import os
import time

# 1. 網頁基本配置
st.set_page_config(page_title="YouTube 下載器 (強化版)", page_icon="🎬")

# 介面標題
st.title("🎬 YouTube 高清影片下載工具 (強化版)")
st.markdown("---")

# 2. 用戶輸入
url = st.text_input("📌 請貼上 YouTube 影片網址 (例如: https://www.youtube.com/watch?v=...)", placeholder="https://...")

if url:
    try:
        # 設定下載後的臨時檔名
        save_path = f"video_{int(time.time())}.mp4"
        
        # --- 核心下載設定 (2024 最新強化偽裝版) ---
        ydl_opts = {
            'format': 'best',  # 下載最高畫質的單一檔案
            'outtmpl': save_path,
            'quiet': True,
            'no_warnings': True,
            # 加入瀏覽器偽裝，減少 403 錯誤
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'referer': 'https://www.google.com/',
            # --- 新增的測試選項 (嘗試繞過 403) ---
            'nocheckcertificate': True,  # 忽略 SSL 證書檢查
            'extractor_args': {
                'youtube': {
                    'player_client': ['android', 'web'] # 嘗試切換不同的客戶端身份
                }
            },
            # -----------------------------------
        }

        with st.status("🚀 正在與 YouTube 伺服器連線...", expanded=True) as status:
            st.write("正在解析影片資訊...")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # 提取影片資訊
                info = ydl.extract_info(url, download=True)
                video_title = info.get('title', 'video')
                video_thumbnail = info.get('thumbnail', None)
                
            status.update(label="✅ 處理完成！", state="complete", expanded=False)

        # 3. 顯示結果與下載按鈕
        if os.path.exists(save_path):
            st.success(f"🎥 準備就緒：{video_title}")
            
            # 如果有縮圖則顯示
            if video_thumbnail:
                st.image(video_thumbnail, width=300)
            
            with open(save_path, "rb") as f:
                st.download_button(
                    label="📥 點擊這裡儲存影片",
                    data=f,
                    file_name=f"{video_title}.mp4",
                    mime="video/mp4",
                    use_container_width=True
                )
            
            # 任務完成後清理伺服器空間
            os.remove(save_path)

    except Exception as e:
        error_msg = str(e)
        st.error("❌ 下載失敗")
        
        if "403" in error_msg:
            st.warning("⚠️ 錯誤代碼 403：YouTube 暫時封鎖了這個伺服器的 IP 地址。")
            st.info("💡 解決建議：\n1. 等待 10-20 分鐘後再試。\n2. 嘗試更換另一個影片網址。\n3. 如果持續失敗，請考慮使用你之前提到的「自建伺服器」方案，因為公用 IP 的封鎖有時會持續幾天。")
        else:
            # 顯示具體錯誤內容
            st.code(error_msg)

# 頁尾說明
st.markdown("---")
st.caption("⚠️ 本工具僅供學術交流及個人備份使用，請尊重影片創作者版權。")
