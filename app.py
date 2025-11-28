import streamlit as st
import os
import time
import uuid
from modules.scene_splitter import SceneSplitter
from modules.image_generator import ImageGenerator
from modules.storyboard_renderer import StoryboardRenderer
from modules.utils import ensure_dirs

# =====================================================
# Streamlit Page Configuration
# =====================================================
st.set_page_config(
    page_title="Neural Storyboard Generator",
    layout="wide",
)

st.markdown("""
<style>
    .block-container { max-width: 1100px; padding: 2rem; }
    .stButton>button { background-color: #4CAF50; color: white; border-radius: 8px; border: none; }
    .stButton>button:hover { background-color: #3e8e41; }
    .scene-box { background-color: #123524; padding: 1rem; border-radius: 8px; margin-bottom: 1rem; color: white; }
    .success-box { background-color: #0d331f; padding: 1rem; border-radius: 8px; color: #aaffc2; font-weight: bold; margin-top: 1rem; }
</style>
""", unsafe_allow_html=True)

st.title("🎬 Neural Storyboard Generator")
st.write("Generate storyboard panels from a short text story using AI.")
st.divider()

# =====================================================
# Initialize Session State
# =====================================================
if "generated" not in st.session_state:
    st.session_state.generated = False
if "captions" not in st.session_state:
    st.session_state.captions = []
if "image_paths" not in st.session_state:
    st.session_state.image_paths = []
# CHANGED: We now track a LIST of storyboard pages, not just one file
if "storyboard_pages" not in st.session_state:
    st.session_state.storyboard_pages = []
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())[:8]

# =====================================================
# User Input
# =====================================================
story = st.text_area(
    "Enter your story:",
    placeholder="Paste a story (can be long, e.g. 20-30 sentences)...",
    height=200
)

col1, col2 = st.columns([1, 5])
with col1:
    generate_btn = st.button("Generate Storyboard")
with col2:
    st.write("") # Spacer

# =====================================================
# LOGIC: GENERATION (Run only when button clicked)
# =====================================================
if generate_btn:
    if not story.strip():
        st.error("Please enter a valid story.")
    else:
        ensure_dirs()
        
        # Reset previous data
        st.session_state.image_paths = []
        st.session_state.storyboard_pages = []
        
        # Setup folders
        session_folder = os.path.join("outputs", st.session_state.session_id)
        images_folder = os.path.join(session_folder, "images")
        storyboard_folder = os.path.join(session_folder, "storyboards")
        
        os.makedirs(images_folder, exist_ok=True)
        os.makedirs(storyboard_folder, exist_ok=True)

        st.info("Processing… This may take a while for long stories.")

        # 1. Split Scenes
        with st.spinner("Splitting story into scenes…"):
            splitter = SceneSplitter()
            # Note: Ensure your config.py MAX_SCENES is set to something high (e.g., 50)
            st.session_state.captions = splitter.split_story(story)

        # 2. Generate Images
        with st.spinner(f"Generating {len(st.session_state.captions)} panels..."):
            gen = ImageGenerator()
            images_data = gen.generate_images(st.session_state.captions)

            # Save individual panels
            for idx, (caption, img) in enumerate(images_data, start=1):
                img_path = os.path.join(images_folder, f"panel_{idx:02d}.png")
                img.save(img_path)
                st.session_state.image_paths.append(img_path)

        # 3. Render Storyboard (Pagination Support)
        with st.spinner("Composing pages..."):
            renderer = StoryboardRenderer()
            # The updated renderer returns a LIST of paths
            # make sure rows_per_page matches your preference
            pages = renderer.render(images_data, out_dir=storyboard_folder, rows_per_page=3)
            st.session_state.storyboard_pages = pages

        # Mark as done
        st.session_state.generated = True
        st.rerun() 

# =====================================================
# LOGIC: DISPLAY
# =====================================================
if st.session_state.generated:
    
    st.markdown("<div class='scene-box'><b>Scenes extracted:</b></div>", unsafe_allow_html=True)
    with st.expander("View all captions"):
        for i, cap in enumerate(st.session_state.captions, 1):
            st.write(f"**Scene {i}:** {cap}")

    st.markdown("<div class='success-box'>Storyboard generated successfully!</div>", unsafe_allow_html=True)

    # --- NEW: Display Multiple Pages ---
    if st.session_state.storyboard_pages:
        st.write(f"**Total Pages:** {len(st.session_state.storyboard_pages)}")
        
        for i, page_path in enumerate(st.session_state.storyboard_pages):
            st.divider()
            st.subheader(f"📄 Page {i+1}")
            
            if os.path.exists(page_path):
                st.image(page_path, use_container_width=True)

                # Download Button for this specific page
                with open(page_path, "rb") as f:
                    st.download_button(
                        label=f"Download Page {i+1}",
                        data=f.read(),
                        file_name=f"storyboard_page_{i+1}_{st.session_state.session_id}.png",
                        mime="image/png",
                        key=f"dl_{i}"
                    )
    else:
        st.warning("No storyboard pages were returned.")

    st.divider()
    st.write(f"Session ID: `{st.session_state.session_id}`")