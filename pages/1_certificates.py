import streamlit as st
from supabase import create_client
import os
from datetime import date as date_cls

st.set_page_config(
    page_title="Certificates",
    page_icon="📜",
    layout="wide"
)

supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)

os.makedirs("data", exist_ok=True)

CERT_FILES_BUCKET = "certificate_files"

CATEGORY_COLORS = {
    "AI": "#6E5BA8",
    "Machine Learning": "#2A8C82",
    "Programming": "#1B2A4A",
    "Workshop": "#C77F1C",
    "Other": "#D8654F",
}

# ---------------------------------------------------------------------------
# Dark mode
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

# ---------------------------------------------------------------------------
# Styling
# ---------------------------------------------------------------------------
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@600;700;800&family=Inter:wght@400;500;600&display=swap');

html, body, [class*="css"] {{ font-family: 'Inter', sans-serif; }}
#MainMenu, footer, header {{visibility: hidden;}}
.stApp {{ background: {bg_gradient}; }}
.block-container {{ padding-top: 2rem; max-width: 1100px; }}

.hero {{
    background: {hero_grad};
    border-radius: 18px;
    padding: 2.5rem 2.5rem;
    margin-bottom: 2rem;
    color: #F7F5F2;
}}
.hero h1 {{ font-family: 'Sora', sans-serif; font-weight: 800; font-size: 2.2rem; margin-bottom: 0.3rem; }}
.hero p {{ color: #C9D3E8; font-size: 1.05rem; margin: 0; }}

.section-label {{
    font-family: 'Sora', sans-serif;
    font-weight: 700;
    font-size: 1.4rem;
    color: {text_main};
    margin: 1.8rem 0 1rem 0;
}}

.cert-card {{
    background: {card_bg};
    border: 1px solid {card_border};
    border-radius: 16px;
    padding: 1.6rem;
    margin-bottom: 1.3rem;
    box-shadow: 0 2px 10px rgba(0,0,0,0.06);
    transition: box-shadow 0.2s ease, transform 0.2s ease;
}}
.cert-card:hover {{
    box-shadow: 0 10px 26px rgba(0,0,0,0.14);
    transform: translateY(-2px);
}}

.cert-title {{
    font-family: 'Sora', sans-serif;
    font-weight: 700;
    font-size: 1.3rem;
    color: {text_main};
    margin-bottom: 0.3rem;
}}

.cert-meta {{
    color: {text_muted};
    font-size: 0.92rem;
    margin: 0.15rem 0;
}}

.badge {{
    display: inline-block;
    border-radius: 999px;
    padding: 0.25rem 0.85rem;
    font-size: 0.78rem;
    font-weight: 600;
    color: white;
    margin-top: 0.5rem;
}}

.no-image-box {{
    height: 140px;
    border-radius: 12px;
    background: {empty_bg};
    border: 1px dashed {card_border};
    display: flex;
    align-items: center;
    justify-content: center;
    color: {text_muted};
    font-size: 0.85rem;
}}

.stButton button, .stLinkButton a {{ border-radius: 8px; font-weight: 600; }}
.streamlit-expanderHeader {{ font-family: 'Sora', sans-serif; font-weight: 600; color: {text_main}; }}

.empty-state {{
    text-align: center;
    padding: 3rem 1rem;
    color: {text_muted};
    background: {empty_bg};
    border-radius: 16px;
    border: 1px dashed {card_border};
}}

[data-testid="stSidebar"] {{ background: {card_bg}; }}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Hero
# ---------------------------------------------------------------------------
st.markdown("""
<div class="hero">
    <h1>📜 My Certificates</h1>
    <p>Learning journey & achievements</p>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Add certificate
# ---------------------------------------------------------------------------
with st.expander("➕ Add Certificate", expanded=False):
    with st.form("add_cert_form", clear_on_submit=True):
        col_a, col_b = st.columns(2)
        with col_a:
            name = st.text_input("Certificate Name *")
            organization = st.text_input("Organization")
            cert_date = st.date_input("Issue Date", value=date_cls.today())
        with col_b:
            category = st.selectbox("Category", list(CATEGORY_COLORS.keys()))
            link = st.text_input("Credential Link")
            image = st.file_uploader("Certificate Image", type=["png", "jpg", "jpeg"])

        attachments = st.file_uploader(
            "Attach files (e.g. certificate PDF + transcript — any number)",
            accept_multiple_files=True
        )

        submitted = st.form_submit_button("Save Certificate", use_container_width=True)

        if submitted:
            if not name.strip():
                st.error("Certificate name is required.")
            else:
                image_path = ""
                if image:
                    image_path = "data/" + image.name
                    with open(image_path, "wb") as f:
                        f.write(image.getbuffer())

                file_urls = []
                for file in attachments:
                    storage_path = f"{name.strip().replace(' ', '_')}_{file.name}"
                    try:
                        supabase.storage.from_(CERT_FILES_BUCKET).upload(
                            storage_path, file.getvalue(), {"content-type": file.type or "application/octet-stream"}
                        )
                        public_url = supabase.storage.from_(CERT_FILES_BUCKET).get_public_url(storage_path)
                        file_urls.append(public_url)
                    except Exception as e:
                        st.warning(f"Couldn't upload {file.name}: {e}")

                supabase.table("certificates").insert({
                    "name": name.strip(),
                    "organization": organization.strip(),
                    "date": str(cert_date),
                    "category": category,
                    "link": link.strip(),
                    "image": image_path,
                    "files": ",".join(file_urls)
                }).execute()

                st.success("Certificate added 🎉")
                st.rerun()

# ---------------------------------------------------------------------------
# Display certificates
# ---------------------------------------------------------------------------
st.markdown('<div class="section-label">🏆 My Certificates</div>', unsafe_allow_html=True)

certificates = supabase.table("certificates").select("*").execute()

if not certificates.data:
    st.markdown('<div class="empty-state">No certificates yet — add your first one above.</div>', unsafe_allow_html=True)
else:
    for cert in certificates.data:
        badge_color = CATEGORY_COLORS.get(cert["category"], "#1B2A4A")

        with st.container():
            st.markdown('<div class="cert-card">', unsafe_allow_html=True)

            col1, col2 = st.columns([1, 2])

            with col1:
                if cert["image"] and os.path.exists(cert["image"]):
                    st.image(cert["image"], use_container_width=True)
                else:
                    st.markdown('<div class="no-image-box">No image</div>', unsafe_allow_html=True)

            with col2:
                st.markdown(f'<div class="cert-title">🏆 {cert["name"]}</div>', unsafe_allow_html=True)
                st.markdown(f'<p class="cert-meta">🏢 {cert["organization"]}</p>', unsafe_allow_html=True)
                st.markdown(f'<p class="cert-meta">📅 {cert["date"]}</p>', unsafe_allow_html=True)
                st.markdown(
                    f'<span class="badge" style="background:{badge_color};">{cert["category"]}</span>',
                    unsafe_allow_html=True
                )

                st.write("")
                if cert["link"]:
                    st.link_button("🔗 View Credential", cert["link"])

                file_urls = [f.strip() for f in (cert.get("files") or "").split(",") if f.strip()]
                if file_urls:
                    st.markdown("**📎 Attached files**")
                    for url in file_urls:
                        fname = url.split("/")[-1]
                        st.link_button(f"📄 {fname}", url, use_container_width=True)

            st.markdown('</div>', unsafe_allow_html=True)

            action_cols = st.columns([2, 1, 1, 1])
            with action_cols[1]:
                share_clicked = st.button("📤 Share", key=f"share_cert_{cert['id']}", use_container_width=True)
            with action_cols[2]:
                delete_clicked = st.button("🗑 Delete", key=f"delete_cert_{cert['id']}", use_container_width=True)
            with action_cols[3]:
                edit_open = st.button("✏️ Edit", key=f"edit_toggle_{cert['id']}", use_container_width=True)

            share_key = f"show_share_cert_{cert['id']}"
            if share_clicked:
                st.session_state[share_key] = not st.session_state.get(share_key, False)

            if st.session_state.get(share_key, False):
                shareable_links = list(file_urls)
                if cert.get("link"):
                    shareable_links.insert(0, cert["link"])
                if not shareable_links:
                    st.caption("No shareable links yet — add a credential link or attach a file first.")
                else:
                    st.caption("Copy any link below to share this certificate elsewhere:")
                    for link_item in shareable_links:
                        st.code(link_item, language=None)

            if delete_clicked:
                supabase.table("certificates").delete().eq("id", cert["id"]).execute()
                if cert["image"] and os.path.exists(cert["image"]):
                    os.remove(cert["image"])
                st.success("Certificate deleted")
                st.rerun()

            edit_key = f"show_edit_{cert['id']}"
            if edit_open:
                st.session_state[edit_key] = not st.session_state.get(edit_key, False)

            if st.session_state.get(edit_key, False):
                with st.form(f"edit_form_{cert['id']}"):
                    new_name = st.text_input("Certificate Name", cert["name"])
                    new_org = st.text_input("Organization", cert["organization"])
                    new_category = st.selectbox(
                        "Category",
                        list(CATEGORY_COLORS.keys()),
                        index=list(CATEGORY_COLORS.keys()).index(cert["category"])
                        if cert["category"] in CATEGORY_COLORS else 0
                    )
                    new_link = st.text_input("Credential Link", cert["link"] or "")

                    if st.form_submit_button("Update Certificate", use_container_width=True):
                        supabase.table("certificates").update({
                            "name": new_name.strip(),
                            "organization": new_org.strip(),
                            "category": new_category,
                            "link": new_link.strip()
                        }).eq("id", cert["id"]).execute()

                        st.session_state[edit_key] = False
                        st.success("Certificate updated")
                        st.rerun()

            st.write("")