#!/usr/bin/env python
"""
Beautiful Streamlit UI for AI Research Pipeline
Black & White Theme with Glassmorphism
"""

import streamlit as st
import sys
import os
from datetime import datetime
from src.crew import Information_Gatherer_Crew

# Page configuration
st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Custom CSS for glassmorphism and black/white theme
st.markdown(
    """
<style>
    /* Main background */
    .main {
        background: linear-gradient(135deg, #000000 0%, #1a1a1a 50%, #000000 100%);
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Title styling */
    .title {
        font-size: 3.5rem;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(90deg, #ffffff 0%, #888888 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
        text-shadow: 0 0 30px rgba(255, 255, 255, 0.3);
    }

    .subtitle {
        text-align: center;
        color: #cccccc;
        font-size: 1.2rem;
        margin-bottom: 40px;
    }

    /* Input field styling - Glass effect */
    .stTextInput input {
        background: rgba(255, 255, 255, 0.08) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 15px !important;
        color: white !important;
        font-size: 1.1rem !important;
        padding: 20px !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
    }

    .stTextInput input:focus {
        border: 2px solid rgba(255, 255, 255, 0.5) !important;
        box-shadow: 0 0 20px rgba(255, 255, 255, 0.2) !important;
    }

    /* Button styling */
    .stButton button {
        background: linear-gradient(135deg, #ffffff 0%, #888888 100%) !important;
        color: black !important;
        border: none !important;
        border-radius: 15px !important;
        padding: 15px 40px !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(255, 255, 255, 0.3) !important;
    }

    .stButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 25px rgba(255, 255, 255, 0.4) !important;
    }

    /* Progress bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, #ffffff 0%, #888888 100%) !important;
    }

    /* Expander styling */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.05) !important;
        border-radius: 10px !important;
        color: white !important;
    }

    /* Status badges */
    .status-badge {
        display: inline-block;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: 600;
        margin: 5px;
        backdrop-filter: blur(10px);
    }

    .status-success {
        background: rgba(0, 255, 0, 0.2);
        border: 1px solid rgba(0, 255, 0, 0.5);
        color: #00ff00;
    }

    .status-processing {
        background: rgba(255, 255, 255, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.5);
        color: #ffffff;
    }

    .status-error {
        background: rgba(255, 0, 0, 0.2);
        border: 1px solid rgba(255, 0, 0, 0.5);
        color: #ff0000;
    }

    /* Settings panel */
    .settings-box {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 15px;
        padding: 25px;
        margin-bottom: 30px;
        backdrop-filter: blur(10px);
    }
</style>
""",
    unsafe_allow_html=True,
)


def update_env_file(obsidian_host, obsidian_api_key):
    """Update .env file with new settings"""
    env_path = ".env"

    # Read existing .env
    env_vars = {}
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    env_vars[key] = value

    # Update values
    env_vars["OBSIDIAN_HOST"] = obsidian_host
    env_vars["OBSIDIAN_API_KEY"] = obsidian_api_key

    # Write back
    with open(env_path, "w") as f:
        for key, value in env_vars.items():
            f.write(f"{key}={value}\n")

    # Reload environment
    os.environ["OBSIDIAN_HOST"] = obsidian_host
    os.environ["OBSIDIAN_API_KEY"] = obsidian_api_key


def run_research_pipeline(topic):
    """
    Run the research pipeline - exactly like main.py
    """
    try:
        # Progress tracking
        progress_bar = st.progress(0)
        status_text = st.empty()

        # Stage 1: Initialize
        status_text.markdown(
            '<div class="status-badge status-processing">🤖 Initializing AI agents...</div>',
            unsafe_allow_html=True,
        )
        progress_bar.progress(10)

        crew_instance = Information_Gatherer_Crew()
        crew = crew_instance.crew()

        # Stage 2: Research
        status_text.markdown(
            '<div class="status-badge status-processing">🔍 Research Agent investigating...</div>',
            unsafe_allow_html=True,
        )
        progress_bar.progress(25)

        # Stage 3: Execute - THE KEY LINE FROM main.py
        with st.spinner("📝 Markdown Agent formatting..."):
            progress_bar.progress(50)

            # This is the exact line from your working main.py
            result = crew.kickoff(inputs={"topic": topic})

            progress_bar.progress(75)

        # Stage 4: Complete
        status_text.markdown(
            '<div class="status-badge status-success">✅ Complete!</div>',
            unsafe_allow_html=True,
        )
        progress_bar.progress(100)

        return True, result

    except Exception as e:
        status_text.markdown(
            '<div class="status-badge status-error">❌ Error</div>',
            unsafe_allow_html=True,
        )
        return False, str(e)


# Header
st.markdown('<h1 class="title">🤖 AI Research Assistant</h1>', unsafe_allow_html=True)
st.markdown(
    '<p class="subtitle">Automatically research any topic and organize it in your Obsidian vault</p>',
    unsafe_allow_html=True,
)

# Settings Panel (Expandable)
with st.expander("⚙️ Settings", expanded=False):
    st.markdown('<div class="settings-box">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        obsidian_host = st.text_input(
            "🌐 Obsidian Host",
            value=os.getenv("OBSIDIAN_HOST", "http://localhost:27124"),
            help="Your Obsidian REST API endpoint. Use localhost for local setup.",
            key="host_input",
        )

    with col2:
        obsidian_api_key = st.text_input(
            "🔑 Obsidian API Key",
            value=os.getenv("OBSIDIAN_API_KEY", ""),
            type="password",
            help="Your Obsidian REST API key from the plugin settings",
            key="key_input",
        )

    if st.button("💾 Save Settings"):
        update_env_file(obsidian_host, obsidian_api_key)
        st.success("✅ Settings saved to .env file!")

    st.markdown("</div>", unsafe_allow_html=True)

# Main content
st.markdown("<br>", unsafe_allow_html=True)

# Research input
col1, col2 = st.columns([4, 1])

with col1:
    research_topic = st.text_input(
        "",
        placeholder="🔍 Enter your research topic... (e.g., 'Quantum Computing', 'Machine Learning')",
        label_visibility="collapsed",
        key="topic_input",
    )

with col2:
    start_button = st.button(
        "🚀 Research", disabled=not research_topic, use_container_width=True
    )

# Execute research when button is clicked
if start_button and research_topic:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 📊 Research Progress")

    # Run the pipeline (same as main.py)
    success, result = run_research_pipeline(research_topic)

    st.markdown("<br>", unsafe_allow_html=True)

    if success:
        st.markdown("### ✅ Research Complete!")
        st.markdown("---")

        # Display results
        with st.expander("📄 View Results", expanded=True):
            st.text_area("Output", value=str(result), height=400, key="result_output")

        # Link to Obsidian
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.success("🎉 Your research has been added to your Obsidian vault!")
            if st.button("📂 Open Obsidian Vault", use_container_width=True):
                st.info("🔗 Open your Obsidian app to view the new research note!")
    else:
        st.error(f"❌ Error occurred: {result}")
        st.markdown("### 💡 Troubleshooting tips:")
        st.markdown("""
        - Check your .env file for correct API keys
        - Ensure Obsidian vault path is configured
        - Verify MCP server is running
        - Check your internet connection
        """)

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown(
    '<p style="text-align: center; color: #888888;">Made with 🤖 by AI Research Assistant | Powered by CrewAI & Obsidian MCP</p>',
    unsafe_allow_html=True,
)
