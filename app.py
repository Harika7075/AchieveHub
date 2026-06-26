import streamlit as st
from supabase import create_client
import random

st.set_page_config(
    page_title="AchieveHub",
    page_icon="🏆",
    layout="wide"
)

supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)

MOTIVATIONAL_QUOTES = [
    "Every certificate is proof you didn't quit.",
    "Small wins, tracked consistently, become a career.",
    "Your future resume is being written today.",
    "Progress, not perfection.",
]

# App-style purple palette (PhonePe-inspired)
PRIMARY = "#5F259F"
PRIMARY_DARK = "#3D1766"
ACCENT = "#FF7A00"

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False
dark = st.session_state.dark_mode

if dark:
    bg = "#0F0B1A"
    card_bg = "#1C1530"
    card_border = "#2E2348"
    text_main = "#F2EEFB"
    text_muted = "#A79CC4"
    empty_bg = "#161024"
    track_bg = "#2E2348"
else:
    bg = "#F4F1FA"
    card_bg = "#FFFFFF"
    card_border = "#E7E0F5"
    text_main = "#241A3D"
    text_muted = "#6B5F8A"
    empty_bg = "#F8F6FC"
    track_bg = "#E7E0F5"

PAGE_PATHS = {
    "home": "app.py",
    "profile": "pages/3_Portfolio.py",
    "projects": "pages/2_projects.py",
    "certificates": "pages/1_certificates.py",
    "achievements": "pages/4_Achievements.py",
    "resume": "pages/5_Resume_Generator.py",
}

# ---------------------------------------------------------------------------
# Styling — app shell look
# ---------------------------------------------------------------------------
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@600;700;800&family=Inter:wght@400;500;600&display=swap');

html, body, [class*="css"] {{ font-family: 'Inter', sans-serif; }}
#MainMenu, footer, header {{visibility: hidden;}}
.stApp {{ background: {bg}; }}
.block-container {{ padding-top: 0rem; padding-bottom: 6rem; max-width: 900px; }}

/* Top app bar */
.app-bar {{
    background: linear-gradient(135deg, {PRIMARY} 0%, {PRIMARY_DARK} 100%);
    border-radius: 0 0 24px 24px;
    padding: 1.4rem 1.6rem 2.2rem 1.6rem;
    margin: 0 -1rem 1.2rem -1rem;
    color: white;
}}
.app-bar-top {{
    display: flex;
    justify-content: space-between;
    align-items: center;
}}
.app-bar-brand {{
    font-family: 'Sora', sans-serif;
    font-weight: 800;
    font-size: 1.3rem;
}}
.app-bar-greeting {{
    margin-top: 1rem;
    font-size: 1.5rem;
    font-weight: 700;
    font-family: 'Sora', sans-serif;
}}
.app-bar-quote {{
    margin-top: 0.3rem;
    font-size: 0.88rem;
    color: rgba(255,255,255,0.75);
    font-style: italic;
}}

/* Balance-style summary card, floating over the app bar */
.summary-card {{
    background: {card_bg};
    border-radius: 18px;
    padding: 1.1rem 1.4rem;
    margin: -1.6rem 0.4rem 1.4rem 0.4rem;
    box-shadow: 0 8px 24px rgba(95,37,159,0.18);
    display: flex;
    justify-content: space-between;
    align-items: center;
}}
.summary-pct {{
    font-family: 'Sora', sans-serif;
    font-weight: 800;
    font-size: 1.6rem;
    color: {PRIMARY};
}}
.summary-label {{ color: {text_muted}; font-size: 0.78rem; font-weight: 600; text-transform: uppercase; }}
.summary-track {{
    height: 8px; width: 100%; background: {track_bg};
    border-radius: 999px; overflow: hidden; margin-top: 0.4rem;
}}
.summary-fill {{
    height: 100%; background: linear-gradient(90deg, {PRIMARY}, {ACCENT});
    border-radius: 999px;
}}

.section-label {{
    font-family: 'Sora', sans-serif;
    font-weight: 700;
    font-size: 1.05rem;
    color: {text_main};
    margin: 1.6rem 0.4rem 0.7rem 0.4rem;
}}

/* Icon tile grid — PhonePe "services" style */
.tile {{
    background: {card_bg};
    border: 1px solid {card_border};
    border-radius: 16px;
    padding: 1rem 0.6rem;
    text-align: center;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}}
.tile:hover {{ transform: translateY(-3px); box-shadow: 0 8px 18px rgba(95,37,159,0.15); }}
.tile-icon-wrap {{
    width: 46px; height: 46px;
    border-radius: 14px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.4rem;
    margin: 0 auto 0.5rem auto;
}}
.tile-label {{
    font-size: 0.78rem;
    font-weight: 600;
    color: {text_main};
}}

/* Stat pills row */
.stat-card {{
    background: {card_bg};
    border: 1px solid {card_border};
    border-radius: 16px;
    padding: 1rem;
    text-align: center;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}}
.stat-value {{ font-family: 'Sora', sans-serif; font-weight: 800; font-size: 1.5rem; color: {PRIMARY}; }}
.stat-label {{ font-size: 0.75rem; color: {text_muted}; font-weight: 600; }}

/* Recent activity list (transaction-list style) */
.activity-row {{
    background: {card_bg};
    border: 1px solid {card_border};
    border-radius: 14px;
    padding: 0.9rem 1.1rem;
    margin-bottom: 0.6rem;
    display: flex;
    align-items: center;
    gap: 0.8rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.03);
}}
.activity-icon {{
    width: 38px; height: 38px;
    border-radius: 10px;
    background: {empty_bg};
    display: flex; align-items: center; justify-content: center;
    font-size: 1.1rem;
}}
.activity-title {{ font-weight: 600; color: {text_main}; font-size: 0.92rem; }}
.activity-meta {{ color: {text_muted}; font-size: 0.78rem; }}

/* Bottom nav bar */
.bottom-nav-spacer {{ height: 70px; }}
.bottom-nav {{
    position: fixed;
    bottom: 0; left: 0; right: 0;
    background: {card_bg};
    border-top: 1px solid {card_border};
    box-shadow: 0 -4px 16px rgba(0,0,0,0.08);
    z-index: 999;
    padding: 0.5rem 0.5rem 0.7rem 0.5rem;
}}

.stButton button, .stLinkButton a {{ border-radius: 10px; font-weight: 600; }}

.empty-state {{
    text-align: center;
    padding: 2rem 1rem;
    color: {text_muted};
    background: {empty_bg};
    border-radius: 16px;
    border: 1px dashed {card_border};
}}

[data-testid="stSidebar"] {{ background: {card_bg}; }}
</style>
""", unsafe_allow_html=True)


def fetch_table(table_name: str):
    try:
        result = supabase.table(table_name).select("*").execute()
        return result.data
    except Exception:
        return []


profiles = fetch_table("profiles")
projects = fetch_table("projects")
certificates = fetch_table("certificates")
achievements = fetch_table("achievements")

profile = profiles[0] if profiles else None
student_name = profile.get("name", "").split(" ")[0] if profile and profile.get("name") else None

project_count = len(projects)
certificate_count = len(certificates)
achievement_count = len(achievements)

skill_count = 0
if profile:
    skills_raw = profile.get("skills", "") or ""
    skill_count = len([s.strip() for s in skills_raw.split(",") if s.strip()])

checklist = {
    "Profile created": bool(profile),
    "About filled in": bool(profile and profile.get("about")),
    "At least 1 skill": skill_count > 0,
    "At least 1 project": project_count > 0,
    "At least 1 certificate": certificate_count > 0,
}
completion_pct = int((sum(checklist.values()) / len(checklist)) * 100)

# ---------------------------------------------------------------------------
# Top app bar
# ---------------------------------------------------------------------------
greeting = f"Hi {student_name} 👋" if student_name else "Hi there 👋"
quote = random.choice(MOTIVATIONAL_QUOTES)

st.markdown(f"""
<div class="app-bar">
    <div class="app-bar-top">
        <div class="app-bar-brand">🏆 AchieveHub</div>
    </div>
    <div class="app-bar-greeting">{greeting}</div>
    <div class="app-bar-quote">“{quote}”</div>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### ⚙️ Display")
    st.session_state.dark_mode = st.toggle("🌙 Dark mode", value=st.session_state.dark_mode)

# ---------------------------------------------------------------------------
# Summary card (floats over the app bar, like a balance card)
# ---------------------------------------------------------------------------
st.markdown(f"""
<div class="summary-card">
    <div>
        <div class="summary-label">Profile Completeness</div>
        <div class="summary-track"><div class="summary-fill" style="width:{completion_pct}%;"></div></div>
    </div>
    <div class="summary-pct">{completion_pct}%</div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Quick actions — icon tile grid
# ---------------------------------------------------------------------------
st.markdown('<div class="section-label">Quick Actions</div>', unsafe_allow_html=True)

tile_cols = st.columns(5)
tiles = [
    ("👤", "Profile", "#EDE4FB", "profile"),
    ("💻", "Projects", "#FFE8D6", "projects"),
    ("📜", "Certs", "#DCF3EE", "certificates"),
    ("🏆", "Goals", "#FFF0D6", "achievements"),
    ("📄", "Resume", "#FBE4EC", "resume"),
]

for col, (icon, label, tile_bg, page_key) in zip(tile_cols, tiles):
    with col:
        st.markdown(f"""
        <div class="tile">
            <div class="tile-icon-wrap" style="background:{tile_bg};">{icon}</div>
            <div class="tile-label">{label}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open", key=f"tile_{page_key}", use_container_width=True):
            try:
                st.switch_page(PAGE_PATHS[page_key])
            except Exception:
                st.info(f"Update PAGE_PATHS['{page_key}'] to match your actual filename.")

# ---------------------------------------------------------------------------
# Stats row
# ---------------------------------------------------------------------------
st.markdown('<div class="section-label">Your Stats</div>', unsafe_allow_html=True)

stat_cols = st.columns(4)
stats = [
    (certificate_count, "Certificates"),
    (project_count, "Projects"),
    (achievement_count, "Achievements"),
    (skill_count, "Skills"),
]
for col, (value, label) in zip(stat_cols, stats):
    with col:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{value}</div>
            <div class="stat-label">{label}</div>
        </div>
        """, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Recent activity — transaction-list style
# ---------------------------------------------------------------------------
st.markdown('<div class="section-label">Recent Activity</div>', unsafe_allow_html=True)

recent_items = []
if certificates:
    c = certificates[-1]
    recent_items.append(("📜", c.get("name", ""), c.get("organization", "")))
if projects:
    p = projects[-1]
    recent_items.append(("💻", p.get("name", ""), p.get("tech", "")))
if achievements:
    a = achievements[-1]
    recent_items.append(("🏆", a.get("title", ""), a.get("organization", "")))

if not recent_items:
    st.markdown('<div class="empty-state">No activity yet — tap a tile above to get started.</div>', unsafe_allow_html=True)
else:
    for icon, title, subtitle in recent_items:
        st.markdown(f"""
        <div class="activity-row">
            <div class="activity-icon">{icon}</div>
            <div>
                <div class="activity-title">{title}</div>
                <div class="activity-meta">{subtitle}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Bottom navigation bar
# ---------------------------------------------------------------------------
st.markdown('<div class="bottom-nav-spacer"></div>', unsafe_allow_html=True)
st.markdown('<div class="bottom-nav">', unsafe_allow_html=True)
nav_cols = st.columns(5)
nav_items = [
    ("🏠", "Home", "home"),
    ("💻", "Projects", "projects"),
    ("📜", "Certs", "certificates"),
    ("🏆", "Goals", "achievements"),
    ("📄", "Resume", "resume"),
]
for col, (icon, label, page_key) in zip(nav_cols, nav_items):
    with col:
        if st.button(f"{icon}\n{label}", key=f"nav_{page_key}", use_container_width=True):
            try:
                st.switch_page(PAGE_PATHS[page_key])
            except Exception:
                st.info(f"Update PAGE_PATHS['{page_key}'] to match your actual filename.")
st.markdown('</div>', unsafe_allow_html=True)