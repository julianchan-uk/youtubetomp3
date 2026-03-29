import streamlit as st
import requests

# 1. 網頁基本配置
st.set_page_config(page_title="YouTube 下載器 (OMV 專屬)", page_icon="🎬")

st.title("🎬 YouTube 影片下載工具 (OMV 測試版)")
st.info("💡 嘗試透過 Tailscale 內網 IP 連接你的 OMV 伺服器。")

# --- 這裡填入你剛才截圖看到的 OMV Tailscale IP ---
OMV_IP = "100.96.125.62" 
OMV_PORT = "8888"

# 2. 用戶輸入
url = st.text_input("📌 請貼上 YouTube 影片網址", placeholder="https://www.youtube.com/watch?v=...")

if url:
    try:
        # 顯示正在處理的狀態
        with st.status("🚀 正在向 OMV (100.96.125.62) 發送指令...", expanded=True) as status:
            # 構建 OMV API 的網址
            api_url = f"http://{OMV_IP}:{OMV_PORT}/download"
            
            # 發送 GET 請求給 OMV
            # 注意：這裡 timeout 設長一點，因為下載影片需要時間
            response = requests.get(api_url, params={"url": url}, timeout=300)
            
            if response.status_code == 200:
                status.update(label="✅ OMV 已成功下載並傳回檔案！", state="complete", expanded=False)
                
                # 提供下載按鈕
                st.download_button(
                    label="📥 點擊這裡儲存影片",
                    data=response.content,
                    file_name="video.mp4",
                    mime="video/mp4",
                    use_container_width=True
                )
            else:
                st.error(f"❌ OMV 傳回錯誤代碼: {response.status_code}")
                st.write(f"錯誤詳情: {response.text}")
                
    except requests.exceptions.Timeout:
        st.error("❌ 連線超時：OMV 下載時間過長，或網路不穩。")
    except requests.exceptions.ConnectionError:
        st.error("❌ 連線失敗：Streamlit 無法透過 Tailscale IP 找到你的 OMV。")
        st.warning("這代表 Streamlit 伺服器與你的家網互不相通，這在雲端平台上是正常的。")
    except Exception as e:
        st.error(f"❌ 發生意外錯誤：{str(e)}")

st.markdown("---")
st.caption(f"目標伺服器：{OMV_IP}:{OMV_PORT} (Tailscale)")
