import streamlit as st
from supabase import create_client
import os

st.set_page_config(
    page_title="Projects",
    page_icon="💻",
    layout="wide"
)

supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)

os.makedirs("data", exist_ok=True)

PROJECT_FILES_BUCKET = "project_files"
PROJECT_IMAGES_BUCKET = "project_images"


def upload_image_to_storage(file, bucket: str) -> str:
    try:
        supabase.storage.from_(bucket).upload(
            file.name, file.getvalue(), {"content-type": file.type or "image/jpeg"}
        )
        return supabase.storage.from_(bucket).get_public_url(file.name)
    except Exception as e:
        st.warning(f"Couldn't upload {file.name}: {e}")
        return ""

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
    chip_bg = "#23304A"
    chip_text = "#9FB4DE"
    chip_border = "#33456B"
else:
    bg_gradient = "radial-gradient(circle at 10% 0%, #EAF0FF 0%, #F7F5F2 35%, #FBF0DA 100%)"
    card_bg = "#FFFFFF"
    card_border = "#E7E2D8"
    text_main = "#1B2A4A"
    text_muted = "#3E4A5E"
    hero_grad = "linear-gradient(135deg, #1B2A4A 0%, #2E4374 100%)"
    empty_bg = "#FBFAF7"
    chip_bg = "#EAF0FF"
    chip_text = "#2E4374"
    chip_border = "#D2DEF7"

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

.project-card {{
    background: {card_bg};
    border: 1px solid {card_border};
    border-radius: 16px;
    padding: 1.6rem;
    margin-bottom: 1.3rem;
    box-shadow: 0 2px 10px rgba(0,0,0,0.06);
    transition: box-shadow 0.2s ease, transform 0.2s ease;
}}
.project-card:hover {{
    box-shadow: 0 10px 26px rgba(0,0,0,0.14);
    transform: translateY(-2px);
}}

.project-title {{
    font-family: 'Sora', sans-serif;
    font-weight: 700;
    font-size: 1.35rem;
    color: {text_main};
    margin-bottom: 0.3rem;
}}

.project-desc {{
    color: {text_muted};
    font-size: 0.95rem;
    line-height: 1.45;
    margin: 0.3rem 0 0.6rem 0;
}}

.tech-chip-row {{ margin: 0.4rem 0 0.8rem 0; }}
.tech-chip {{
    display: inline-block;
    background: {chip_bg};
    color: {chip_text};
    border: 1px solid {chip_border};
    border-radius: 999px;
    padding: 0.25rem 0.75rem;
    font-size: 0.8rem;
    font-weight: 500;
    margin: 0 0.35rem 0.35rem 0;
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
    <h1>💻 My Projects</h1>
    <p>My development journey 🚀</p>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Add project
# ---------------------------------------------------------------------------
with st.expander("➕ Add Project", expanded=False):
    with st.form("add_project_form", clear_on_submit=True):
        name = st.text_input("Project Name *")
        description = st.text_area("Project Description", height=90)

        col_a, col_b = st.columns(2)
        with col_a:
            tech = st.text_input("Tech Stack (comma-separated)")
            github = st.text_input("GitHub Link")
        with col_b:
            demo = st.text_input("Demo Link")
            image = st.file_uploader("Project Image", type=["png", "jpg", "jpeg"])

        attachments = st.file_uploader(
            "Attach files (PDFs, docs, zips, extra images — any number)",
            accept_multiple_files=True
        )

        submitted = st.form_submit_button("🚀 Save Project", use_container_width=True)

        if submitted:
            if not name.strip():
                st.error("Project name is required.")
            else:
                image_url = ""
                if image:
                    image_url = upload_image_to_storage(image, PROJECT_IMAGES_BUCKET)

                file_urls = []
                for file in attachments:
                    storage_path = f"{name.strip().replace(' ', '_')}_{file.name}"
                    try:
                        supabase.storage.from_(PROJECT_FILES_BUCKET).upload(
                            storage_path, file.getvalue(), {"content-type": file.type or "application/octet-stream"}
                        )
                        public_url = supabase.storage.from_(PROJECT_FILES_BUCKET).get_public_url(storage_path)
                        file_urls.append(public_url)
                    except Exception as e:
                        st.warning(f"Couldn't upload {file.name}: {e}")

                supabase.table("projects").insert({
                    "name": name.strip(),
                    "description": description.strip(),
                    "tech": tech.strip(),
                    "github": github.strip(),
                    "demo": demo.strip(),
                    "image": image_url,
                    "files": ",".join(file_urls)
                }).execute()

                st.success("Project added successfully 🎉")
                st.rerun()

# ---------------------------------------------------------------------------
# Display projects
# ---------------------------------------------------------------------------
st.markdown('<div class="section-label">🌟 My Projects</div>', unsafe_allow_html=True)

projects = supabase.table("projects").select("*").execute()

if not projects.data:
    st.markdown('<div class="empty-state">No projects yet — add your first one above.</div>', unsafe_allow_html=True)
else:
    for project in projects.data:
        with st.container():
            st.markdown('<div class="project-card">', unsafe_allow_html=True)

            col1, col2 = st.columns([1, 2])

            with col1:
                if project.get("image"):
                    st.image(project["image"], use_container_width=True)
                else:
                    st.markdown('<div class="no-image-box">No image</div>', unsafe_allow_html=True)

            with col2:
                st.markdown(f'<div class="project-title">🌱 {project["name"]}</div>', unsafe_allow_html=True)

                if project["description"]:
                    st.markdown(f'<p class="project-desc">{project["description"]}</p>', unsafe_allow_html=True)

                if project["tech"]:
                    chips = "".join(
                        f'<span class="tech-chip">{t.strip()}</span>'
                        for t in project["tech"].split(",") if t.strip()
                    )
                    st.markdown(f'<div class="tech-chip-row">{chips}</div>', unsafe_allow_html=True)

                link_cols = st.columns([1, 1, 4])
                with link_cols[0]:
                    if project["github"]:
                        st.link_button("🔗 GitHub", project["github"], use_container_width=True)
                with link_cols[1]:
                    if project["demo"]:
                        st.link_button("🚀 Demo", project["demo"], use_container_width=True)

                # Attached files (PDFs, docs, zips, etc.)
                file_urls = [f.strip() for f in (project.get("files") or "").split(",") if f.strip()]
                if file_urls:
                    st.markdown("**📎 Attached files**")
                    for url in file_urls:
                        fname = url.split("/")[-1]
                        st.link_button(f"📄 {fname}", url, use_container_width=True)

            st.markdown('</div>', unsafe_allow_html=True)

            # Delete / Edit / View / Share — correctly scoped INSIDE the loop for this project
            action_cols = st.columns([1, 1, 1, 1])
            with action_cols[0]:
                if st.button("🔍 View Details", key=f"view_proj_{project['id']}", use_container_width=True):
                    st.session_state["details_type"] = "project"
                    st.session_state["details_id"] = str(project["id"])
                    st.query_params["type"] = "project"
                    st.query_params["id"] = str(project["id"])
                    st.switch_page("pages/6_Details.py")
            with action_cols[1]:
                share_clicked = st.button("📤 Share", key=f"share_proj_{project['id']}", use_container_width=True)
            with action_cols[2]:
                delete_clicked = st.button("🗑 Delete", key=f"delete_proj_{project['id']}", use_container_width=True)
            with action_cols[3]:
                edit_toggle = st.button("✏️ Edit", key=f"edit_toggle_proj_{project['id']}", use_container_width=True)

            share_key = f"show_share_proj_{project['id']}"
            if share_clicked:
                st.session_state[share_key] = not st.session_state.get(share_key, False)

            if st.session_state.get(share_key, False):
                shareable_links = list(file_urls)
                if project.get("github"):
                    shareable_links.insert(0, project["github"])
                if not shareable_links:
                    st.caption("No shareable links yet — add a GitHub link or attach a file first.")
                else:
                    st.caption("Copy any link below to share this project elsewhere:")
                    for link in shareable_links:
                        st.code(link, language=None)

            if delete_clicked:
                supabase.table("projects").delete().eq("id", project["id"]).execute()
                st.success("Project deleted")
                st.rerun()

            edit_key = f"show_edit_proj_{project['id']}"
            if edit_toggle:
                st.session_state[edit_key] = not st.session_state.get(edit_key, False)

            if st.session_state.get(edit_key, False):
                with st.form(f"edit_proj_form_{project['id']}"):
                    new_name = st.text_input("Edit Name", project["name"])
                    new_description = st.text_area("Edit Description", project["description"])
                    new_tech = st.text_input("Edit Tech Stack", project["tech"])
                    new_github = st.text_input("Edit GitHub Link", project["github"] or "")
                    new_demo = st.text_input("Edit Demo Link", project["demo"] or "")

                    if st.form_submit_button("Update Project", use_container_width=True):
                        supabase.table("projects").update({
                            "name": new_name.strip(),
                            "description": new_description.strip(),
                            "tech": new_tech.strip(),
                            "github": new_github.strip(),
                            "demo": new_demo.strip()
                        }).eq("id", project["id"]).execute()

                        st.session_state[edit_key] = False
                        st.success("Project updated")
                        st.rerun()

            st.write("")