import streamlit as st
from supabase import create_client
import os

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    HRFlowable,
    Table,
    TableStyle
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white
import datetime

st.set_page_config(
    page_title="Resume Generator",
    page_icon="📄",
    layout="wide"
)

supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)

# ---------------------------------------------------------------------------
# Auth gate — must be logged in to view this page
# ---------------------------------------------------------------------------
if "user" not in st.session_state or st.session_state.user is None:
    st.warning("Please log in from the Home page first.")
    st.stop()

current_user_id = st.session_state.user.id

os.makedirs("data", exist_ok=True)

ACCENT_OPTIONS = {
    "Navy": "#1B2A4A",
    "Amber": "#C77F1C",
    "Teal": "#2A8C82",
    "Coral": "#D8654F",
    "Violet": "#6E5BA8",
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

.settings-card, .preview-box {{
    background: {card_bg};
    border: 1px solid {card_border};
    border-radius: 16px;
    padding: 1.6rem;
    box-shadow: 0 2px 10px rgba(0,0,0,0.06);
    margin-bottom: 1.3rem;
}}

.stat-pill {{
    display: inline-block;
    background: {empty_bg};
    border: 1px solid {card_border};
    border-radius: 999px;
    padding: 0.3rem 0.9rem;
    font-size: 0.82rem;
    font-weight: 600;
    color: {text_main};
    margin: 0 0.4rem 0.4rem 0;
}}

.stButton button, .stDownloadButton button {{ border-radius: 8px; font-weight: 600; }}

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

# ---------------------------------------------------------------------------
# Hero
# ---------------------------------------------------------------------------
st.markdown("""
<div class="hero">
    <h1>📄 Resume Generator</h1>
    <p>Turn your portfolio into a ready-to-share PDF resume</p>
</div>
""", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Data fetching — always scoped to the logged-in student
# ---------------------------------------------------------------------------
def fetch_own_table(table_name: str):
    """Fetch only the current student's rows from a table; [] if none or table missing."""
    try:
        result = (
            supabase.table(table_name)
            .select("*")
            .eq("user_id", current_user_id)
            .execute()
        )
        return result.data
    except Exception:
        return []


def build_resume_text(profile_data, project_data, cert_data, achievement_data, sections: dict) -> str:
    resume = ""

    if profile_data:
        p = profile_data[0]
        resume += f"{p.get('name', '')}\n\n"

        contact_bits = [p.get("github", ""), p.get("linkedin", "")]
        contact_bits = [c for c in contact_bits if c]
        if contact_bits:
            resume += " | ".join(contact_bits) + "\n\n"

        if sections.get("about") and p.get("about"):
            resume += f"ABOUT\n{p['about']}\n\n"
        if sections.get("education") and p.get("education"):
            resume += f"EDUCATION\n{p['education']}\n\n"
        if sections.get("goal") and p.get("goal"):
            resume += f"GOAL\n{p['goal']}\n\n"
        if sections.get("skills") and p.get("skills"):
            resume += f"SKILLS\n{p['skills']}\n\n"

    if sections.get("projects") and project_data:
        resume += "PROJECTS\n\n"
        for proj in project_data:
            resume += f"- {proj.get('name', '')}: {proj.get('description', '')}\n"
            if proj.get("tech"):
                resume += f"  Tech: {proj['tech']}\n"
        resume += "\n"

    if sections.get("certificates") and cert_data:
        resume += "CERTIFICATES\n\n"
        for cert in cert_data:
            line = f"- {cert.get('name', '')}"
            if cert.get("organization"):
                line += f" ({cert['organization']})"
            resume += line + "\n"
        resume += "\n"

    if sections.get("achievements") and achievement_data:
        resume += "ACHIEVEMENTS\n\n"
        for ach in achievement_data:
            resume += f"- {ach.get('title', '')}\n"
        resume += "\n"

    return resume.strip()


def create_resume_pdf(profile_data, project_data, cert_data, achievement_data, sections: dict,
                       accent_hex: str, template: str, output_path: str) -> str:
    doc = SimpleDocTemplate(
        output_path, pagesize=A4,
        topMargin=16 * mm, bottomMargin=18 * mm,
        leftMargin=18 * mm, rightMargin=18 * mm
    )
    base_styles = getSampleStyleSheet()
    page_width = A4[0] - 36 * mm

    body_style = base_styles["BodyText"]
    bullet_style = ParagraphStyle(
        "BulletStyle", parent=base_styles["BodyText"], leftIndent=10, spaceAfter=2
    )

    p = profile_data[0] if profile_data else {}
    contact_bits = [p.get("github", ""), p.get("linkedin", "")]
    contact_bits = [c for c in contact_bits if c]

    content = []

    if template == "Modern":
        # Colored header banner with name in white
        name_style = ParagraphStyle(
            "NameStyleModern", parent=base_styles["Title"],
            textColor=white, fontSize=22, alignment=0, spaceAfter=2
        )
        contact_style = ParagraphStyle(
            "ContactStyleModern", parent=base_styles["BodyText"],
            textColor=white, fontSize=9.5
        )
        header_cell = [Paragraph(p.get("name", ""), name_style)]
        if contact_bits:
            header_cell.append(Paragraph(" &nbsp;|&nbsp; ".join(contact_bits), contact_style))

        header_table = Table([[header_cell]], colWidths=[page_width])
        header_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), HexColor(accent_hex)),
            ("LEFTPADDING", (0, 0), (-1, -1), 14),
            ("RIGHTPADDING", (0, 0), (-1, -1), 14),
            ("TOPPADDING", (0, 0), (-1, -1), 14),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
        ]))
        content.append(header_table)
        content.append(Spacer(1, 14))

        def add_heading(text):
            bar = Table([[Paragraph(f"<b>{text}</b>", ParagraphStyle(
                "ModernHeading", parent=base_styles["Heading4"], textColor=white, fontSize=10.5
            ))]], colWidths=[page_width])
            bar.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), HexColor(accent_hex)),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]))
            content.append(Spacer(1, 8))
            content.append(bar)
            content.append(Spacer(1, 4))

    else:  # Classic
        name_style = ParagraphStyle(
            "NameStyleClassic", parent=base_styles["Title"],
            textColor=HexColor(accent_hex), fontSize=22, spaceAfter=2
        )
        contact_style = ParagraphStyle(
            "ContactStyleClassic", parent=base_styles["BodyText"],
            textColor=HexColor("#555555"), fontSize=9.5, spaceAfter=10
        )
        if p.get("name"):
            content.append(Paragraph(p["name"], name_style))
        if contact_bits:
            content.append(Paragraph(" &nbsp;|&nbsp; ".join(contact_bits), contact_style))
        content.append(HRFlowable(width="100%", color=HexColor(accent_hex), thickness=1.2))
        content.append(Spacer(1, 6))

        def add_heading(text):
            heading_style = ParagraphStyle(
                "ClassicHeading", parent=base_styles["Heading3"],
                textColor=HexColor(accent_hex), spaceBefore=10, spaceAfter=4
            )
            content.append(Paragraph(text, heading_style))

    if sections.get("about") and p.get("about"):
        add_heading("ABOUT")
        content.append(Paragraph(p["about"], body_style))

    if sections.get("education") and p.get("education"):
        add_heading("EDUCATION")
        content.append(Paragraph(p["education"], body_style))

    if sections.get("goal") and p.get("goal"):
        add_heading("CAREER GOAL")
        content.append(Paragraph(p["goal"], body_style))

    if sections.get("skills") and p.get("skills"):
        add_heading("SKILLS")
        content.append(Paragraph(p["skills"], body_style))

    if sections.get("projects") and project_data:
        add_heading("PROJECTS")
        for proj in project_data:
            line = f"<b>{proj.get('name', '')}</b> — {proj.get('description', '')}"
            content.append(Paragraph(line, bullet_style))
            if proj.get("tech"):
                content.append(Paragraph(f"<i>Tech: {proj['tech']}</i>", bullet_style))

    if sections.get("certificates") and cert_data:
        add_heading("CERTIFICATES")
        for cert in cert_data:
            line = cert.get("name", "")
            if cert.get("organization"):
                line += f" — {cert['organization']}"
            content.append(Paragraph(line, bullet_style))

    if sections.get("achievements") and achievement_data:
        add_heading("ACHIEVEMENTS")
        for ach in achievement_data:
            content.append(Paragraph(ach.get("title", ""), bullet_style))

    doc.build(content)
    return output_path


# ---------------------------------------------------------------------------
# Resume history (Supabase Storage) — scoped to the current student
# ---------------------------------------------------------------------------
RESUME_BUCKET = "resumes"


def save_resume_to_history(pdf_path: str, template: str, accent_hex: str):
    """Upload the generated PDF to Supabase Storage and log it in resume_history for this student."""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    storage_path = f"{current_user_id}_resume_{timestamp}.pdf"

    with open(pdf_path, "rb") as f:
        file_bytes = f.read()

    supabase.storage.from_(RESUME_BUCKET).upload(
        storage_path, file_bytes, {"content-type": "application/pdf"}
    )

    public_url = supabase.storage.from_(RESUME_BUCKET).get_public_url(storage_path)

    supabase.table("resume_history").insert({
        "user_id": current_user_id,
        "file_path": storage_path,
        "file_url": public_url,
        "template": template,
        "accent_color": accent_hex,
    }).execute()

    return public_url


def fetch_resume_history():
    try:
        result = (
            supabase.table("resume_history")
            .select("*")
            .eq("user_id", current_user_id)
            .order("id", desc=True)
            .execute()
        )
        return result.data
    except Exception:
        return []


def delete_resume_history_entry(entry_id, file_path):
    try:
        supabase.storage.from_(RESUME_BUCKET).remove([file_path])
    except Exception:
        pass
    supabase.table("resume_history").delete().eq("id", entry_id).eq("user_id", current_user_id).execute()


# ---------------------------------------------------------------------------
# Load data — only the current student's own profile, projects, certs, achievements
# ---------------------------------------------------------------------------
profiles = fetch_own_table("profiles")
projects = fetch_own_table("projects")
certificates = fetch_own_table("certificates")
achievements = fetch_own_table("achievements")

if not profiles:
    st.markdown(
        '<div class="empty-state">No profile found yet — create one on the Portfolio page first.</div>',
        unsafe_allow_html=True
    )
else:
    # -----------------------------------------------------------------
    # Settings: sections to include + accent color
    # -----------------------------------------------------------------
    st.markdown('<div class="section-label">⚙️ Resume Settings</div>', unsafe_allow_html=True)
    st.markdown('<div class="settings-card">', unsafe_allow_html=True)

    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.markdown("**Sections to include**")
        sec_cols = st.columns(3)
        with sec_cols[0]:
            inc_about = st.checkbox("About", value=True)
            inc_education = st.checkbox("Education", value=True)
        with sec_cols[1]:
            inc_goal = st.checkbox("Career goal", value=True)
            inc_skills = st.checkbox("Skills", value=True)
        with sec_cols[2]:
            inc_projects = st.checkbox("Projects", value=True)
            inc_certs = st.checkbox("Certificates", value=True)
        inc_achievements = st.checkbox("Achievements", value=True)

    with col_right:
        st.markdown("**Accent color**")
        accent_name = st.selectbox("Accent", list(ACCENT_OPTIONS.keys()), label_visibility="collapsed")
        accent_hex = ACCENT_OPTIONS[accent_name]

        st.markdown("**Template style**")
        template = st.radio("Template", ["Classic", "Modern"], label_visibility="collapsed", horizontal=True)

    st.markdown('</div>', unsafe_allow_html=True)

    sections = {
        "about": inc_about,
        "education": inc_education,
        "goal": inc_goal,
        "skills": inc_skills,
        "projects": inc_projects,
        "certificates": inc_certs,
        "achievements": inc_achievements,
    }

    # -----------------------------------------------------------------
    # Quick stats
    # -----------------------------------------------------------------
    st.markdown(
        f"""
        <span class="stat-pill">📁 {len(projects)} Projects</span>
        <span class="stat-pill">🏆 {len(certificates)} Certificates</span>
        <span class="stat-pill">⭐ {len(achievements)} Achievements</span>
        """,
        unsafe_allow_html=True
    )

    # -----------------------------------------------------------------
    # Generate
    # -----------------------------------------------------------------
    if st.button("🪄 Generate Resume", use_container_width=True):
        st.session_state["resume_text"] = build_resume_text(
            profiles, projects, certificates, achievements, sections
        )
        st.session_state["resume_sections"] = sections
        st.session_state["resume_accent"] = accent_hex
        st.session_state["resume_template"] = template

    if "resume_text" in st.session_state:
        st.markdown('<div class="section-label">📋 Preview & Edit</div>', unsafe_allow_html=True)
        st.markdown('<div class="preview-box">', unsafe_allow_html=True)

        edited_text = st.text_area(
            "Generated Resume (editable before download)",
            st.session_state["resume_text"],
            height=420,
            label_visibility="collapsed"
        )
        st.session_state["resume_text"] = edited_text

        st.markdown('</div>', unsafe_allow_html=True)

        pdf_path = create_resume_pdf(
            profiles, projects, certificates, achievements,
            st.session_state["resume_sections"], st.session_state["resume_accent"],
            st.session_state["resume_template"], "data/resume.pdf"
        )

        dl_cols = st.columns(3)
        with dl_cols[0]:
            with open(pdf_path, "rb") as pdf_file:
                st.download_button(
                    "📥 Download PDF",
                    pdf_file,
                    file_name="Resume.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
        with dl_cols[1]:
            st.download_button(
                "📄 Download as TXT",
                edited_text,
                file_name="Resume.txt",
                mime="text/plain",
                use_container_width=True
            )
        with dl_cols[2]:
            if st.button("💾 Save to History", use_container_width=True):
                try:
                    save_resume_to_history(
                        pdf_path, st.session_state["resume_template"], st.session_state["resume_accent"]
                    )
                    st.success("Saved to history 🎉")
                    st.rerun()
                except Exception as e:
                    st.error(f"Couldn't save to history: {e}")

    # -----------------------------------------------------------------
    # Resume history — only this student's saved resumes
    # -----------------------------------------------------------------
    st.markdown('<div class="section-label">📚 Resume History</div>', unsafe_allow_html=True)

    history = fetch_resume_history()

    if not history:
        st.markdown(
            '<div class="empty-state">No saved resumes yet — generate one above and click "Save to History".</div>',
            unsafe_allow_html=True
        )
    else:
        for entry in history:
            st.markdown('<div class="settings-card">', unsafe_allow_html=True)
            hist_cols = st.columns([3, 1, 1])
            with hist_cols[0]:
                st.markdown(
                    f"**{entry.get('template', 'Classic')} template** &nbsp;·&nbsp; "
                    f"saved {entry.get('created_at', '')[:19].replace('T', ' ')}",
                    unsafe_allow_html=True
                )
            with hist_cols[1]:
                if entry.get("file_url"):
                    st.link_button("📥 Open", entry["file_url"], use_container_width=True)
            with hist_cols[2]:
                if st.button("🗑 Delete", key=f"delete_hist_{entry['id']}", use_container_width=True):
                    delete_resume_history_entry(entry["id"], entry["file_path"])
                    st.success("Deleted from history")
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)