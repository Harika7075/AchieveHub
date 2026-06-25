
import streamlit as st
from supabase import create_client
import requests

st.set_page_config(
    page_title="Details",
    page_icon="🔍",
    layout="wide"
)

supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)

# ---------------------------------------------------------------------------
# Dark mode (shared with other pages)
# ---------------------------------------------------------------------------
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

with st.sidebar:
    st.markdown("### ⚙️ Display")
    st.session_state.dark_mode = st.toggle("🌙 Dark mode", value=st.session_state.dark_mode)

dark = st.session_state.dark_mode

if dark:
    bg_gradient = "radial-gradient(circle at 10% 0%, #18203A 0%, #11151F 45%, #1B1410 100%)"
    card_bg = "#1B2235"
    card_border = "#2C3650"
    text_main = "#E7E9F0"
    text_muted = "#9AA3B8"
    hero_grad = "linear-gradient(135deg, #0F1626 0%, #1B2A4A 100%)"
    empty_bg = "#161B29"
else:
    bg_gradient = "radial-gradient(circle at 10% 0%, #EAF0FF 0%, #F7F5F2 35%, #FBF0DA 100%)"
    card_bg = "#FFFFFF"
    card_border = "#E7E2D8"
    text_main = "#1B2A4A"
    text_muted = "#3E4A5E"
    hero_grad = "linear-gradient(135deg, #1B2A4A 0%, #2E4374 100%)"
    empty_bg = "#FBFAF7"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@600;700;800&family=Inter:wght@400;500;600&display=swap');
html, body, [class*="css"] {{ font-family: 'Inter', sans-serif; }}
#MainMenu, footer, header {{visibility: hidden;}}
.stApp {{ background: {bg_gradient}; }}
.block-container {{ padding-top: 2rem; max-width: 850px; }}

.hero {{
    background: {hero_grad};
    border-radius: 18px;
    padding: 2.2rem 2.5rem;
    margin-bottom: 1.5rem;
    color: #F7F5F2;
}}
.hero h1 {{ font-family: 'Sora', sans-serif; font-weight: 800; font-size: 2rem; margin-bottom: 0.2rem; }}
.hero p {{ color: #C9D3E8; font-size: 1rem; margin: 0; }}

.detail-card {{
    background: {card_bg};
    border: 1px solid {card_border};
    border-radius: 16px;
    padding: 1.8rem;
    box-shadow: 0 2px 10px rgba(0,0,0,0.06);
    margin-bottom: 1.3rem;
}}
.detail-label {{
    font-family: 'Sora', sans-serif;
    font-weight: 600;
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    color: {text_muted};
    margin-top: 0.9rem;
    margin-bottom: 0.15rem;
}}
.detail-text {{ color: {text_main}; font-size: 1rem; line-height: 1.5; margin: 0; }}

.stButton button, .stLinkButton a, .stDownloadButton button {{ border-radius: 8px; font-weight: 600; }}

.empty-state {{
    text-align: center;
    padding: 2.5rem 1rem;
    color: {text_muted};
    background: {empty_bg};
    border-radius: 16px;
    border: 1px dashed {card_border};
}}
[data-testid="stSidebar"] {{ background: {card_bg}; }}
</style>
""", unsafe_allow_html=True)


def download_file_bytes(url: str):
    """Fetch the raw bytes of a file from its public Supabase Storage URL."""
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            return response.content
    except Exception:
        pass
    return None


item_type = st.query_params.get("type")
item_id = st.query_params.get("id")

TYPE_CONFIG = {
    "project": {"table": "projects", "icon": "💻", "title_field": "name"},
    "certificate": {"table": "certificates", "icon": "📜", "title_field": "name"},
    "achievement": {"table": "achievements", "icon": "🏆", "title_field": "title"},
}

if not item_type or not item_id or item_type not in TYPE_CONFIG:
    st.markdown("""
    <div class="hero">
        <h1>🔍 Item Details</h1>
        <p>No item selected</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(
        '<div class="empty-state">Open this page by clicking "View Details" on a project, certificate, or achievement.</div>',
        unsafe_allow_html=True
    )
else:
    config = TYPE_CONFIG[item_type]
    result = supabase.table(config["table"]).select("*").eq("id", item_id).execute()

    if not result.data:
        st.markdown(
            '<div class="empty-state">This item could not be found — it may have been deleted.</div>',
            unsafe_allow_html=True
        )
    else:
        item = result.data[0]
        title = item.get(config["title_field"], "Untitled")

        st.markdown(f"""
        <div class="hero">
            <h1>{config['icon']} {title}</h1>
            <p>Full details</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="detail-card">', unsafe_allow_html=True)

        if item.get("image"):
            # Local path won't exist on a fresh server — show only if it's a URL
            if str(item["image"]).startswith("http"):
                st.image(item["image"], width=300)

        for field in ["description", "about", "organization", "education", "goal",
                      "skills", "tech", "category", "date"]:
            if item.get(field):
                st.markdown(f'<div class="detail-label">{field.replace("_", " ")}</div>', unsafe_allow_html=True)
                st.markdown(f'<p class="detail-text">{item[field]}</p>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        # -------------------------------------------------------------
        # Links
        # -------------------------------------------------------------
        link_fields = {"github": "🔗 GitHub", "demo": "🚀 Demo", "link": "🔗 Reference Link"}
        link_cols = st.columns(3)
        col_idx = 0
        for field, label in link_fields.items():
            if item.get(field):
                with link_cols[col_idx % 3]:
                    st.link_button(label, item[field], use_container_width=True)
                col_idx += 1

        # -------------------------------------------------------------
        # Downloadable files — actual PDF/image bytes, not just links
        # -------------------------------------------------------------
        file_urls = [f.strip() for f in (item.get("files") or "").split(",") if f.strip()]

        if file_urls:
            st.markdown('<div class="detail-label" style="margin-top:1.5rem;">📎 Attached Files</div>', unsafe_allow_html=True)
            for url in file_urls:
                fname = url.split("/")[-1]
                dl_col, link_col = st.columns([2, 1])
                with dl_col:
                    file_bytes = download_file_bytes(url)
                    if file_bytes:
                        st.download_button(
                            f"📥 Download {fname}",
                            data=file_bytes,
                            file_name=fname,
                            use_container_width=True,
                            key=f"dl_{url}"
                        )
                    else:
                        st.caption(f"Couldn't fetch {fname} for download.")
                with link_col:
                    st.link_button("🔗 Open", url, use_container_width=True)
        else:
            st.caption("No files attached to this item.")

        # -------------------------------------------------------------
        # Share this page
        # -------------------------------------------------------------
        st.markdown('<div class="detail-label" style="margin-top:1.5rem;">📤 Share this page</div>', unsafe_allow_html=True)
        current_url = f"?type={item_type}&id={item_id}"
        st.caption("Share this exact link — anyone who opens it sees this same details page:")
        st.code(current_url, language=None)
        st.caption("⚠️ Replace this with your full app URL + the text above (e.g. https://your-app.streamlit.app/Details?type=project&id=12) when sharing outside the app.")