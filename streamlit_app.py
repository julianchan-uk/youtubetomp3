import streamlit as st
import requests
import re

# 網頁配置
st.set_page_config(page_title="私人 YouTube 下載器", page_icon="🎬")

st.title("🎬 私人 YouTube 高清下載 (透過 OMV)")
st.markdown("---")

# --- 修改後的 DDNS 設定 ---
# 使用你的 No-IP 域名，這樣就算不開 Tailscale (只要路由器有做 Port Forwarding) 也能連
OMV_ADDRESS = "chanwaiman.ddns.net"
OMV_PORT = "8888" 
# -------------------------

OMV_API_URL = f"http://{OMV_ADDRESS}:{OMV_PORT}/download"

# 側邊欄檢查連線狀態
st.sidebar.header("📡 伺服器狀態")
try:
    # 檢查 OMV API 是否在線
    health_check = requests.get(f"http://{OMV_ADDRESS}:{OMV_PORT}/", timeout=5)
    if health_check.status_code == 200:
        st.sidebar.success("✅ OMV 後台連線正常")
    else:
        st.sidebar.warning("⚠️ 後台有回應但狀態碼異常")
except Exception:
    st.sidebar.error("❌ 無法連線至 OMV")
    st.sidebar.info(f"💡 請檢查：\n1. 你的路由器是否已將 Port {OMV_PORT} 轉發至 192.168.1.101\n2. OMV 嘅 yt-api 係咪 Up？")

# 用戶輸入
url = st.text_input("📌 請貼上 YouTube 影片網址：", placeholder="https://www.youtube.com/watch?v=...")

if url:
    if st.button("🚀 開始下載"):
        try:
            with st.spinner("🎬 正在通知家中的 OMV 進行下載並傳回，請稍候..."):
                params = {'url': url}
                # 發送請求給 OMV
                response = requests.get(OMV_API_URL, params=params, timeout=600)
                
                if response.status_code == 200:
                    st.success("✅ 下載完成！")
                    
                    # 取得檔名
                    filename = "video.mp4"
                    cd = response.headers.get('content-disposition')
                    if cd:
                        fname_match = re.findall("filename=(.+)", cd)
                        if fname_match: filename = fname_match[0].strip('"')

                    st.download_button(
                        label="📥 儲存影片到電腦 / 手機",
                        data=response.content,
                        file_name=filename,
                        mime="video/mp4",
                        use_container_width=True
                    )
