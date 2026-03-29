import streamlit as st
import requests

# 網頁配置
st.set_page_config(page_title="私人 YouTube 下載器", page_icon="🎬")

st.title("🎬 私人 YouTube 高清下載 (透過 OMV)")
st.markdown("---")

# ---------------------------------------------------------
# ⚠️ 重要設定：請將下方引號內的 IP 換成你部 OMV 嘅 Tailscale IP
# 你可以在 OMV 輸入 `tailscale ip -4` 搵返嗰組 100.x.x.x 嘅數字
OMV_TAILSCALE_IP = "你的_OMV_TAILSCALE_IP" 
# ---------------------------------------------------------

OMV_API_URL = f"http://{OMV_TAILSCALE_IP}:8000/download"

st.sidebar.header("📡 伺服器狀態")
try:
    # 簡單檢查後台是否有反應
    health_check = requests.get(f"http://{OMV_TAILSCALE_IP}:8000/", timeout=3)
    if health_check.status_code == 200:
        st.sidebar.success("✅ OMV 後台已連線")
    else:
        st.sidebar.warning("⚠️ 後台有回應但狀態異常")
except:
    st.sidebar.error("❌ 無法連線至 OMV")
    st.sidebar.info("請確保：\n1. OMV 已啟動 Tailscale\n2. Docker 正在運行\n3. 你的 Tailscale 網絡容許此連線")

# 用戶輸入
url = st.text_input("📌 請貼上 YouTube 影片網址：", placeholder="https://www.youtube.com/watch?v=...")

if url:
    if st.button("🚀 開始解析並下載"):
        try:
            with st.spinner("🎬 正在通知家中的 OMV 進行下載，請稍候..."):
                # 發送請求給 OMV API
                params = {'url': url}
                # YouTube 下載可能需要較長時間，設定超時為 10 分鐘
                response = requests.get(OMV_API_URL, params=params, timeout=600)
                
                if response.status_code == 200:
                    st.success("✅ OMV 下載完成！檔案已準備好。")
                    
                    # 嘗試從 Header 攞檔名
                    filename = "video.mp4"
                    if 'content-disposition' in response.headers:
                        import re
                        fname = re.findall("filename=(.+)", response.headers['content-disposition'])
                        if fname: filename = fname[0].strip('"')

                    st.download_button(
                        label="📥 點擊這裡儲存影片到電腦",
                        data=response.content,
                        file_name=filename,
                        mime="video/mp4",
                        use_container_width=True
                    )
                else:
                    st.error(f"❌ OMV 下載失敗：{response.text}")
                    
        except requests.exceptions.Timeout:
            st.error("❌ 連線超時：影片可能太長，或者家裡網絡上傳速度較慢。")
        except Exception as e:
            st.error(f"❌ 發生錯誤：{str(e)}")

st.markdown("---")
st.caption("後端架構：Streamlit Cloud -> Tailscale Network -> OMV Docker (FastAPI)")
