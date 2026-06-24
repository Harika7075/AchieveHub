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
    "Document the journey — it's more impressive than you think.",
]

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
    hero_grad = "linear-gradient(135deg, #0F1626 0%, #1B2A4A 55%, #4A2E1F 100%)"
    empty_bg = "#161B29"
    track_bg = "#2C3650"
else:
    bg_gradient = "radial-gradient(circle at 10% 0%, #EAF0FF 0%, #F7F5F2 35%, #FBF0DA 100%)"
    card_bg = "#FFFFFF"
    card_border = "#E7E2D8"
    text_main = "#1B2A4A"
    text_muted = "#3E4A5E"
    hero_grad = "linear-gradient(135deg, #1B2A4A 0%, #2E4374 55%, #E8A33D 130%)"
    empty_bg = "#FBFAF7"
    track_bg = "#E7E2D8"

ACCENT = "#E8A33D"

# ---------------------------------------------------------------------------
# Styling
# ---------------------------------------------------------------------------
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@600;700;800&family=Inter:wght@400;500;600&display=swap');

html, body, [class*="css"] {{ font-family: 'Inter', sans-serif; }}
#MainMenu, footer, header {{visibility: hidden;}}
.stApp {{ background: {bg_gradient}; }}
.block-container {{ padding-top: 2rem; max-width: 1150px; }}

/* Hero */
.hero {{
    background: {hero_grad};
    border-radius: 22px;
    padding: 3rem 3rem;
    margin-bottom: 1.5rem;
    color: #F7F5F2;
    position: relative;
    overflow: hidden;
}}
.hero::after {{
    content: "";
    position: absolute;
    top: -60px; right: -60px;
    width: 220px; height: 220px;
    background: rgba(255,255,255,0.06);
    border-radius: 50%;
}}
.hero-eyebrow {{
    color: #E8A33D;
    font-weight: 700;
    font-size: 0.85rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 0.6rem;
}}
.hero h1 {{
    font-family: 'Sora', sans-serif;
    font-weight: 800;
    font-size: 2.6rem;
    margin-bottom: 0.4rem;
    line-height: 1.15;
}}
.hero p {{ color: #C9D3E8; font-size: 1.1rem; margin: 0; max-width: 600px; }}
.hero-quote {{
    margin-top: 1.4rem;
    font-style: italic;
    color: #E8A33D;
    font-size: 0.95rem;
    border-left: 3px solid #E8A33D;
    padding-left: 0.8rem;
}}

.section-label {{
    font-family: 'Sora', sans-serif;
    font-weight: 700;
    font-size: 1.4rem;
    color: {text_main};
    margin: 2rem 0 1rem 0;
}}

/* Progress card */
.progress-card {{
    background: {card_bg};
    border: 1px solid {card_border};
    border-radius: 16px;
    padding: 1.6rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 2px 10px rgba(0,0,0,0.06);
}}
.progress-track {{
    height: 10px;
    width: 100%;
    background: {track_bg};
    border-radius: 999px;
    overflow: hidden;
    margin-top: 0.6rem;
}}
.progress-fill {{
    height: 100%;
    background: linear-gradient(90deg, {ACCENT}, #D8654F);
    border-radius: 999px;
    transition: width 0.4s ease;
}}

/* Metric cards */
.metric-card {{
    background: {card_bg};
    border: 1px solid {card_border};
    border-radius: 16px;
    padding: 1.4rem;
    text-align: center;
    box-shadow: 0 2px 10px rgba(0,0,0,0.06);
    transition: box-shadow 0.2s ease, transform 0.2s ease;
}}
.metric-card:hover {{
    box-shadow: 0 10px 26px rgba(0,0,0,0.14);
    transform: translateY(-3px);
}}
.metric-icon {{ font-size: 1.7rem; margin-bottom: 0.3rem; }}
.metric-value {{
    font-family: 'Sora', sans-serif;
    font-weight: 800;
    font-size: 2.1rem;
    color: {text_main};
}}
.metric-label {{
    color: {text_muted};
    font-size: 0.83rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.03em;
}}

/* Action cards */
.action-card {{
    background: {card_bg};
    border: 1px solid {card_border};
    border-radius: 16px;
    padding: 1.5rem;
    text-align: center;
    box-shadow: 0 2px 10px rgba(0,0,0,0.06);
    transition: box-shadow 0.2s ease, transform 0.2s ease;
    height: 100%;
}}
.action-card:hover {{
    box-shadow: 0 10px 26px rgba(0,0,0,0.14);
    transform: translateY(-3px);
    border-color: {ACCENT};
}}
.action-icon {{ font-size: 2rem; margin-bottom: 0.4rem; }}
.action-title {{
    font-family: 'Sora', sans-serif;
    font-weight: 700;
    color: {text_main};
    font-size: 1.05rem;
}}
.action-sub {{ color: {text_muted}; font-size: 0.82rem; margin-top: 0.2rem; }}

/* Highlight / featured cards */
.highlight-card {{
    background: {card_bg};
    border: 1px solid {card_border};
    border-radius: 16px;
    padding: 1.3rem;
    margin-bottom: 0.9rem;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    border-left: 4px solid {ACCENT};
}}
.highlight-title {{ font-weight: 700; color: {text_main}; font-size: 0.98rem; }}
.highlight-meta {{ color: {text_muted}; font-size: 0.82rem; margin-top: 0.15rem; }}

.stButton button, .stLinkButton a {{ border-radius: 8px; font-weight: 600; }}

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


# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------
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

# ---------------------------------------------------------------------------
# Profile completeness
# ---------------------------------------------------------------------------
checklist = {
    "Profile created": bool(profile),
    "About filled in": bool(profile and profile.get("about")),
    "At least 1 skill": skill_count > 0,
    "At least 1 project": project_count > 0,
    "At least 1 certificate": certificate_count > 0,
}
completed = sum(checklist.values())
total_checks = len(checklist)
completion_pct = int((completed / total_checks) * 100)

# ---------------------------------------------------------------------------
# Hero
# ---------------------------------------------------------------------------
greeting = f"Welcome back, {student_name} 👋" if student_name else "Welcome to AchieveHub 👋"
quote = random.choice(MOTIVATIONAL_QUOTES)

st.markdown(f"""
<div class="hero">
    <div class="hero-eyebrow">🏆 Your Achievement Vault</div>
    <h1>{greeting}</h1>
    <p>Track every project, certificate, and milestone — then turn it into a polished resume in one click.</p>
    <div class="hero-quote">“{quote}”</div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Profile completeness bar
# ---------------------------------------------------------------------------
st.markdown(f"""
<div class="progress-card">
    <div style="display:flex; justify-content:space-between; align-items:center;">
        <span style="font-weight:700; color:{text_main};">Profile Completeness</span>
        <span style="font-weight:700; color:{ACCENT};">{completion_pct}%</span>
    </div>
    <div class="progress-track">
        <div class="progress-fill" style="width:{completion_pct}%;"></div>
    </div>
</div>
""", unsafe_allow_html=True)

if completion_pct < 100:
    missing = [label for label, done in checklist.items() if not done]
    st.caption("Still missing: " + " · ".join(missing))

# ---------------------------------------------------------------------------
# Dashboard metrics
# ---------------------------------------------------------------------------
metric_cols = st.columns(4)
metrics = [
    ("📜", certificate_count, "Certificates"),
    ("💻", project_count, "Projects"),
    ("🏆", achievement_count, "Achievements"),
    ("🎓", skill_count, "Skills"),
]
for col, (icon, value, label) in zip(metric_cols, metrics):
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">{icon}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-label">{label}</div>
        </div>
        """, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Quick actions — real navigation
# ---------------------------------------------------------------------------
st.markdown('<div class="section-label">⚡ Quick Actions</div>', unsafe_allow_html=True)

# NOTE: update these page paths to match your actual filenames under pages/
PAGE_PATHS = {
    "portfolio": "Pages/3_Portfolio.py",
    "projects": "Pages/2_projects.py",
    "certificates": "Pages/1_certificates.py",
    "achievements": "Pages/4_Achievements.py",
    "resume": "Pages/5_Resume_Generator.py",
}


action_cols = st.columns(4)
actions = [
    ("👤", "Edit Portfolio", "Update your bio & skills", "portfolio"),
    ("💻", "Add Project", "Showcase your latest build", "projects"),
    ("📜", "Add Certificate", "Log a new credential", "certificates"),
    ("📄", "Build Resume", "Generate a PDF in seconds", "resume"),
]

for col, (icon, title, sub, page_key) in zip(action_cols, actions):
    with col:
        st.markdown(f"""
        <div class="action-card">
            <div class="action-icon">{icon}</div>
            <div class="action-title">{title}</div>
            <div class="action-sub">{sub}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Go →", key=f"go_{page_key}", use_container_width=True):
            try:
                st.switch_page(PAGE_PATHS[page_key])
            except Exception:
                st.info(f"Update PAGE_PATHS['{page_key}'] in the code to match your actual page filename.")

# ---------------------------------------------------------------------------
# Featured highlights
# ---------------------------------------------------------------------------
st.markdown('<div class="section-label">✨ Featured Highlights</div>', unsafe_allow_html=True)

if not (projects or certificates or achievements):
    st.markdown(
        '<div class="empty-state">Nothing here yet — add your first project, certificate, or achievement to see it featured.</div>',
        unsafe_allow_html=True
    )
else:
    hl_cols = st.columns(3)

    with hl_cols[0]:
        st.markdown("**💻 Latest Project**")
        if projects:
            p = projects[-1]
            st.markdown(f"""
            <div class="highlight-card">
                <div class="highlight-title">{p.get('name', '')}</div>
                <div class="highlight-meta">{p.get('tech', '')}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.caption("No projects yet")

    with hl_cols[1]:
        st.markdown("**📜 Latest Certificate**")
        if certificates:
            c = certificates[-1]
            st.markdown(f"""
            <div class="highlight-card">
                <div class="highlight-title">{c.get('name', '')}</div>
                <div class="highlight-meta">{c.get('organization', '')}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.caption("No certificates yet")

    with hl_cols[2]:
        st.markdown("**🏆 Latest Achievement**")
        if achievements:
            a = achievements[-1]
            st.markdown(f"""
            <div class="highlight-card">
                <div class="highlight-title">{a.get('title', '')}</div>
                <div class="highlight-meta">{a.get('organization', '')}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.caption("No achievements yet")

# ---------------------------------------------------------------------------
# Recent activity summary
# ---------------------------------------------------------------------------
st.markdown('<div class="section-label">🕘 Recent Activity</div>', unsafe_allow_html=True)

if project_count == 0 and certificate_count == 0 and achievement_count == 0:
    st.markdown(
        '<div class="empty-state">No activity yet — your journey starts with one entry.</div>',
        unsafe_allow_html=True
    )
else:
    summary_bits = []
    if project_count:
        summary_bits.append(f"{project_count} project{'s' if project_count != 1 else ''}")
    if certificate_count:
        summary_bits.append(f"{certificate_count} certificate{'s' if certificate_count != 1 else ''}")
    if achievement_count:
        summary_bits.append(f"{achievement_count} achievement{'s' if achievement_count != 1 else ''}")
    st.success(f"You have {', '.join(summary_bits)} logged so far 🎉 Keep going!")