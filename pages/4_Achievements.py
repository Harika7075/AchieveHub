import streamlit as st
from supabase import create_client
import os
from datetime import date as date_cls

st.set_page_config(
    page_title="Achievements",
    page_icon="⭐",
    layout="wide"
)

supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)

os.makedirs("data", exist_ok=True)

ACHIEVEMENT_IMAGES_BUCKET = "achievement_images"


def upload_image_to_storage(file, bucket: str) -> str:
    try:
        supabase.storage.from_(bucket).upload(
            file.name, file.getvalue(), {"content-type": file.type or "image/jpeg"}
        )
        return supabase.storage.from_(bucket).get_public_url(file.name)
    except Exception as e:
        st.warning(f"Couldn't upload {file.name}: {e}")
        return ""

CATEGORY_COLORS = {
    "Award": "#C77F1C",
    "Competition": "#D8654F",
    "Publication": "#2A8C82",
    "Leadership": "#6E5BA8",
    "Other": "#1B2A4A",
}

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

.ach-card {{
    background: {card_bg};
    border: 1px solid {card_border};
    border-radius: 16px;
    padding: 1.6rem;
    margin-bottom: 1.3rem;
    box-shadow: 0 2px 10px rgba(0,0,0,0.06);
    transition: box-shadow 0.2s ease, transform 0.2s ease;
}}
.ach-card:hover {{
    box-shadow: 0 10px 26px rgba(0,0,0,0.14);
    transform: translateY(-2px);
}}

.ach-title {{
    font-family: 'Sora', sans-serif;
    font-weight: 700;
    font-size: 1.3rem;
    color: {text_main};
    margin-bottom: 0.3rem;
}}

.ach-meta {{
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
    <h1>⭐ My Achievements</h1>
    <p>Milestones, awards, and recognitions</p>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Add achievement
# ---------------------------------------------------------------------------
with st.expander("➕ Add Achievement", expanded=False):
    with st.form("add_achievement_form", clear_on_submit=True):
        col_a, col_b = st.columns(2)
        with col_a:
            title = st.text_input("Achievement Title *")
            organization = st.text_input("Organization / Event")
            ach_date = st.date_input("Date", value=date_cls.today())
        with col_b:
            category = st.selectbox("Category", list(CATEGORY_COLORS.keys()))
            link = st.text_input("Reference Link (optional)")
            image = st.file_uploader("Image (optional)", type=["png", "jpg", "jpeg"])

        description = st.text_area("Description (optional)", height=80)

        submitted = st.form_submit_button("Save Achievement", use_container_width=True)

        if submitted:
            if not title.strip():
                st.error("Achievement title is required.")
            else:
                image_url = ""
                if image:
                    image_url = upload_image_to_storage(image, ACHIEVEMENT_IMAGES_BUCKET)

                supabase.table("achievements").insert({
                    "title": title.strip(),
                    "organization": organization.strip(),
                    "date": str(ach_date),
                    "category": category,
                    "link": link.strip(),
                    "description": description.strip(),
                    "image": image_url
                }).execute()

                st.success("Achievement added 🎉")
                st.rerun()

# ---------------------------------------------------------------------------
# Display achievements
# ---------------------------------------------------------------------------
st.markdown('<div class="section-label">🏅 My Achievements</div>', unsafe_allow_html=True)

achievements = supabase.table("achievements").select("*").execute()

if not achievements.data:
    st.markdown('<div class="empty-state">No achievements yet — add your first one above.</div>', unsafe_allow_html=True)
else:
    for ach in achievements.data:
        badge_color = CATEGORY_COLORS.get(ach.get("category"), "#1B2A4A")

        with st.container():
            st.markdown('<div class="ach-card">', unsafe_allow_html=True)

            col1, col2 = st.columns([1, 2])

            with col1:
                if ach.get("image"):
                    st.image(ach["image"], use_container_width=True)
                else:
                    st.markdown('<div class="no-image-box">No image</div>', unsafe_allow_html=True)

            with col2:
                st.markdown(f'<div class="ach-title">⭐ {ach["title"]}</div>', unsafe_allow_html=True)

                if ach.get("organization"):
                    st.markdown(f'<p class="ach-meta">🏢 {ach["organization"]}</p>', unsafe_allow_html=True)
                if ach.get("date"):
                    st.markdown(f'<p class="ach-meta">📅 {ach["date"]}</p>', unsafe_allow_html=True)
                if ach.get("description"):
                    st.markdown(f'<p class="ach-meta">{ach["description"]}</p>', unsafe_allow_html=True)

                if ach.get("category"):
                    st.markdown(
                        f'<span class="badge" style="background:{badge_color};">{ach["category"]}</span>',
                        unsafe_allow_html=True
                    )

                st.write("")
                if ach.get("link"):
                    st.link_button("🔗 View Reference", ach["link"])

            st.markdown('</div>', unsafe_allow_html=True)

            action_cols = st.columns([1, 1, 1])
            with action_cols[0]:
                if st.button("🔍 View Details", key=f"view_ach_{ach['id']}", use_container_width=True):
                    st.session_state["details_type"] = "achievement"
                    st.session_state["details_id"] = str(ach["id"])
                    st.query_params["type"] = "achievement"
                    st.query_params["id"] = str(ach["id"])
                    st.switch_page("pages/6_Details.py")
            with action_cols[1]:
                delete_clicked = st.button("🗑 Delete", key=f"delete_ach_{ach['id']}", use_container_width=True)
            with action_cols[2]:
                edit_open = st.button("✏️ Edit", key=f"edit_toggle_ach_{ach['id']}", use_container_width=True)

            if delete_clicked:
                supabase.table("achievements").delete().eq("id", ach["id"]).execute()
                st.success("Achievement deleted")
                st.rerun()

            edit_key = f"show_edit_ach_{ach['id']}"
            if edit_open:
                st.session_state[edit_key] = not st.session_state.get(edit_key, False)

            if st.session_state.get(edit_key, False):
                with st.form(f"edit_ach_form_{ach['id']}"):
                    new_title = st.text_input("Achievement Title", ach["title"])
                    new_org = st.text_input("Organization / Event", ach.get("organization") or "")
                    new_category = st.selectbox(
                        "Category",
                        list(CATEGORY_COLORS.keys()),
                        index=list(CATEGORY_COLORS.keys()).index(ach["category"])
                        if ach.get("category") in CATEGORY_COLORS else 0
                    )
                    new_link = st.text_input("Reference Link", ach.get("link") or "")
                    new_description = st.text_area("Description", ach.get("description") or "")

                    if st.form_submit_button("Update Achievement", use_container_width=True):
                        supabase.table("achievements").update({
                            "title": new_title.strip(),
                            "organization": new_org.strip(),
                            "category": new_category,
                            "link": new_link.strip(),
                            "description": new_description.strip()
                        }).eq("id", ach["id"]).execute()

                        st.session_state[edit_key] = False
                        st.success("Achievement updated")
                        st.rerun()

            st.write("")