import streamlit as st
from supabase import create_client
import os

st.set_page_config(
    page_title="Student Portfolio",
    page_icon="🎓",
    layout="wide"
)

# ---------------------------------------------------------------------------
# Supabase connection
# ---------------------------------------------------------------------------
supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)

os.makedirs("data", exist_ok=True)

# Available accent colors students can choose from
COLOR_PALETTE = {
    "Navy":   "#1B2A4A",
    "Amber":  "#C77F1C",
    "Teal":   "#2A8C82",
    "Coral":  "#D8654F",
    "Violet": "#6E5BA8",
    "Rose":   "#B5446E",
}

# ---------------------------------------------------------------------------
# Dark mode toggle (top of sidebar)
# ---------------------------------------------------------------------------
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

with st.sidebar:
    st.markdown("### ⚙️ Display")
    st.session_state.dark_mode = st.toggle("🌙 Dark mode", value=st.session_state.dark_mode)

dark = st.session_state.dark_mode

# Theme tokens
if dark:
    bg_gradient = "radial-gradient(circle at 10% 0%, #18203A 0%, #11151F 45%, #1B1410 100%)"
    card_bg = "#1B2235"
    card_border = "#2C3650"
    text_main = "#E7E9F0"
    text_muted = "#9AA3B8"
    hero_grad = "linear-gradient(135deg, #0F1626 0%, #1B2A4A 100%)"
    chip_bg = "#2A2316"
    chip_border = "#4A3A1C"
    chip_text = "#E0B567"
    empty_bg = "#161B29"
else:
    bg_gradient = "radial-gradient(circle at 10% 0%, #EAF0FF 0%, #F7F5F2 35%, #FBF0DA 100%)"
    card_bg = "#FFFFFF"
    card_border = "#E7E2D8"
    text_main = "#1B2A4A"
    text_muted = "#3E4A5E"
    hero_grad = "linear-gradient(135deg, #1B2A4A 0%, #2E4374 100%)"
    chip_bg = "#FBF0DA"
    chip_border = "#F0D9A8"
    chip_text = "#946A1D"
    empty_bg = "#FBFAF7"

# ---------------------------------------------------------------------------
# Styling
# ---------------------------------------------------------------------------
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@600;700;800&family=Inter:wght@400;500;600&display=swap');

html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif;
}}

#MainMenu, footer, header {{visibility: hidden;}}

.stApp {{
    background: {bg_gradient};
}}

.block-container {{
    padding-top: 2rem;
    max-width: 1100px;
}}

.hero {{
    background: {hero_grad};
    border-radius: 18px;
    padding: 2.5rem 2.5rem;
    margin-bottom: 2rem;
    color: #F7F5F2;
}}
.hero h1 {{
    font-family: 'Sora', sans-serif;
    font-weight: 800;
    font-size: 2.2rem;
    margin-bottom: 0.3rem;
}}
.hero p {{
    color: #C9D3E8;
    font-size: 1.05rem;
    margin: 0;
}}

.section-label {{
    font-family: 'Sora', sans-serif;
    font-weight: 700;
    font-size: 1.4rem;
    color: {text_main};
    margin: 1.8rem 0 1rem 0;
}}

/* Profile card */
.profile-card {{
    background: {card_bg};
    border: 1px solid {card_border};
    border-radius: 16px;
    overflow: hidden;
    margin-bottom: 1.5rem;
    box-shadow: 0 2px 10px rgba(0,0,0,0.06);
    transition: box-shadow 0.2s ease, transform 0.2s ease;
}}
.profile-card:hover {{
    box-shadow: 0 10px 26px rgba(0,0,0,0.14);
    transform: translateY(-2px);
}}

/* Cover banner */
.cover-banner {{
    height: 90px;
    width: 100%;
    background-size: cover;
    background-position: center;
}}
.cover-fallback {{
    height: 90px;
    width: 100%;
}}

.card-body {{
    padding: 1.6rem;
    padding-top: 0;
    margin-top: -45px;
}}

.profile-name {{
    font-family: 'Sora', sans-serif;
    font-weight: 700;
    font-size: 1.35rem;
    color: {text_main};
    margin-bottom: 0.2rem;
}}

.profile-field-label {{
    font-family: 'Sora', sans-serif;
    font-weight: 600;
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    margin-top: 0.9rem;
    margin-bottom: 0.15rem;
}}

.profile-field-text {{
    color: {text_muted};
    font-size: 0.95rem;
    line-height: 1.45;
    margin: 0;
}}

.chip-row {{ margin-top: 0.3rem; }}
.chip {{
    display: inline-block;
    background: {chip_bg};
    color: {chip_text};
    border: 1px solid {chip_border};
    border-radius: 999px;
    padding: 0.25rem 0.75rem;
    font-size: 0.82rem;
    font-weight: 500;
    margin: 0 0.35rem 0.35rem 0;
}}

.avatar-wrap img {{
    border-radius: 50%;
    object-fit: cover;
    border: 4px solid {card_bg};
    box-shadow: 0 0 0 1px {card_border};
}}
.avatar-placeholder {{
    width: 110px;
    height: 110px;
    border-radius: 50%;
    color: #F7F5F2;
    font-family: 'Sora', sans-serif;
    font-weight: 700;
    font-size: 2rem;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 4px solid {card_bg};
    box-shadow: 0 0 0 1px {card_border};
}}

.stButton button, .stLinkButton a {{
    border-radius: 8px;
    font-weight: 600;
    font-family: 'Inter', sans-serif;
}}

.streamlit-expanderHeader {{
    font-family: 'Sora', sans-serif;
    font-weight: 600;
    color: {text_main};
}}

.empty-state {{
    text-align: center;
    padding: 3rem 1rem;
    color: {text_muted};
    background: {empty_bg};
    border-radius: 16px;
    border: 1px dashed {card_border};
}}

[data-testid="stSidebar"] {{
    background: {card_bg};
}}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Hero header
# ---------------------------------------------------------------------------
st.markdown("""
<div class="hero">
    <h1>🎓 Student Portfolio</h1>
    <p>Showcase your story, skills, and goals — all in one place.</p>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Create profile
# ---------------------------------------------------------------------------
with st.expander("➕ Create your profile", expanded=False):
    with st.form("create_profile_form", clear_on_submit=True):
        col_a, col_b = st.columns(2)
        with col_a:
            name = st.text_input("Name *")
            education = st.text_input("Education")
            github = st.text_input("GitHub link")
        with col_b:
            goal = st.text_input("Career goal")
            skills = st.text_input("Skills (comma-separated)")
            linkedin = st.text_input("LinkedIn link")

        about = st.text_area("About", height=100)

        color_name = st.selectbox("Accent color", list(COLOR_PALETTE.keys()))

        img_col, cover_col = st.columns(2)
        with img_col:
            image = st.file_uploader("Profile image", type=["png", "jpg", "jpeg"])
        with cover_col:
            cover = st.file_uploader("Cover banner (optional)", type=["png", "jpg", "jpeg"])

        submitted = st.form_submit_button("Save profile", use_container_width=True)

        if submitted:
            st.write({
    "name": name,
    "about": about,
    "education": education,
    "goal": goal,
    "skills": skills,
    "github": github,
    "linkedin": linkedin
})
            if not name.strip():
                st.error("Name is required.")
            else:
                image_path = ""
                if image:
                    image_path = "data/" + image.name
                    with open(image_path, "wb") as f:
                        f.write(image.getbuffer())

                cover_path = ""
                if cover:
                    cover_path = "data/cover_" + cover.name
                    with open(cover_path, "wb") as f:
                        f.write(cover.getbuffer())

                supabase.table("profiles").insert({
                    "name": name.strip(),
                    "about": about.strip(),
                    "education": education.strip(),
                    "goal": goal.strip(),
                    "skills": skills.strip(),
                    "github": github.strip(),
                    "linkedin": linkedin.strip(),
                    "image": image_path,
                    "cover_image": cover_path,
                    "accent_color": COLOR_PALETTE[color_name],
                }).execute()

                st.success("Profile created 🎉")
                st.rerun()

# ---------------------------------------------------------------------------
# Display profiles
# ---------------------------------------------------------------------------
st.markdown('<div class="section-label">🌟 Student Profiles</div>', unsafe_allow_html=True)

profiles = supabase.table("profiles").select("*").execute()

if not profiles.data:
    st.markdown("""
    <div class="empty-state">
        No profiles yet — create the first one above.
    </div>
    """, unsafe_allow_html=True)
else:
    for profile in profiles.data:
        accent = profile.get("accent_color") or "#1B2A4A"
        cover_path = profile.get("cover_image")

        with st.container():
            st.markdown('<div class="profile-card">', unsafe_allow_html=True)

            # Cover banner — image if present, else solid accent color
            if cover_path and os.path.exists(cover_path):
                st.markdown(
                    f'<div class="cover-banner" style="background-image:url(\'{cover_path}\');"></div>',
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f'<div class="cover-fallback" style="background:{accent};"></div>',
                    unsafe_allow_html=True
                )

            st.markdown('<div class="card-body">', unsafe_allow_html=True)

            col1, col2 = st.columns([1, 3])

            with col1:
                if profile["image"] and os.path.exists(profile["image"]):
                    st.markdown('<div class="avatar-wrap">', unsafe_allow_html=True)
                    st.image(profile["image"], width=110)
                    st.markdown('</div>', unsafe_allow_html=True)
                else:
                    initial = profile["name"][0].upper() if profile["name"] else "?"
                    st.markdown(
                        f'<div class="avatar-placeholder" style="background:{accent};">{initial}</div>',
                        unsafe_allow_html=True
                    )

            with col2:
                st.markdown(f'<div class="profile-name">{profile["name"]}</div>', unsafe_allow_html=True)

                if profile["about"]:
                    st.markdown(f'<div class="profile-field-label" style="color:{accent};">About</div>', unsafe_allow_html=True)
                    st.markdown(f'<p class="profile-field-text">{profile["about"]}</p>', unsafe_allow_html=True)

                field_cols = st.columns(2)
                with field_cols[0]:
                    if profile["education"]:
                        st.markdown(f'<div class="profile-field-label" style="color:{accent};">Education</div>', unsafe_allow_html=True)
                        st.markdown(f'<p class="profile-field-text">{profile["education"]}</p>', unsafe_allow_html=True)
                with field_cols[1]:
                    if profile["goal"]:
                        st.markdown(f'<div class="profile-field-label" style="color:{accent};">Career goal</div>', unsafe_allow_html=True)
                        st.markdown(f'<p class="profile-field-text">{profile["goal"]}</p>', unsafe_allow_html=True)

                if profile["skills"]:
                    st.markdown(f'<div class="profile-field-label" style="color:{accent};">Skills</div>', unsafe_allow_html=True)
                    chips = "".join(
                        f'<span class="chip">{s.strip()}</span>'
                        for s in profile["skills"].split(",") if s.strip()
                    )
                    st.markdown(f'<div class="chip-row">{chips}</div>', unsafe_allow_html=True)

                st.write("")
                link_cols = st.columns([1, 1, 4])
                with link_cols[0]:
                    if profile["github"]:
                        st.link_button("🔗 GitHub", profile["github"], use_container_width=True)
                with link_cols[1]:
                    if profile["linkedin"]:
                        st.link_button("💼 LinkedIn", profile["linkedin"], use_container_width=True)

            st.markdown('</div>', unsafe_allow_html=True)  # close card-body
            st.markdown('</div>', unsafe_allow_html=True)  # close profile-card

            # Delete button — INSIDE the loop, scoped to this profile
            del_col = st.columns([5, 1])[1]
            with del_col:
                if st.button("🗑 Delete", key=f"delete_{profile['id']}", use_container_width=True):
                    supabase.table("profiles").delete().eq("id", profile["id"]).execute()
                    if profile["image"] and os.path.exists(profile["image"]):
                        os.remove(profile["image"])
                    if cover_path and os.path.exists(cover_path):
                        os.remove(cover_path)
                    st.success("Profile deleted")
                    st.rerun()