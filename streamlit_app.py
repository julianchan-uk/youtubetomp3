import streamlit as st
import requests
import re

# 網頁配置
st.set_page_config(page_title="私人 YouTube 下載器", page_icon="🎬")

st.title("🎬 私人 YouTube 高清下載 (透過 OMV)")
st.markdown("---")

# --- 自動填入你部 OMV 嘅 Tailscale IP ---
OMV_TAILSCALE_IP = "100.96.125.62" 
# --------------------------------------

OMV_API_URL = f"http://{OMV_TAILSCALE_IP}:8000/download"

# 側邊欄檢查連線狀態
st.sidebar.header("📡 伺服器狀態")
try:
    # 檢查 OMV API 是否在線 (Timeout 設短一點)
    health_check = requests.get(f"http://{OMV_TAILSCALE_IP}:8000/", timeout=5)
    if health_check.status_code == 200:
        st.sidebar.success("✅ OMV 後台連線正常")
    else:
        st.sidebar.warning("⚠️ 後台有回應但狀態碼異常")
except Exception:
    st.sidebar.error("❌ 無法連線至 OMV")
    st.sidebar.info("💡 請檢查：\n1. 你部電腦係咪開咗 Tailscale？\n2. OMV 嘅 yt-api 係咪 Up？")

# 用戶輸入
url = st.text_input("📌 請貼上 YouTube 影片網址：", placeholder="https://www.youtube.com/watch?v=...")

if url:
    if st.button("🚀 開始下載"):
        try:
            with st.spinner("🎬 正在通知家中的 OMV 進行下載並傳回，請稍候..."):
                # 發送請求，設定較長的 Timeout (10分鐘) 給大型影片
                params = {'url': url}
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
                else:
                    st.error(f"❌ OMV 報錯：{response.text}")
                    
        except Exception as e:
            st.error(f"❌ 連線失敗：{str(e)}")
            st.info("💡 貼士：如果你喺出面用緊 5G，記得你部手機都要開住 Tailscale App 先連到返屋企部 OMV 㗎！")

st.markdown("---")
st.caption(f"Backend: {OMV_TAILSCALE_IP} | Port: 8000")
