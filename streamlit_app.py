import streamlit as st
import os
from youtube_search import YouTubeSearchAgent
from gemini_summary import GeminiSummaryAgent
from dotenv import load_dotenv
import json
import time

# Load environment variables
load_dotenv()

# Page configuration with custom theme
st.set_page_config(
    page_title="Video Learning Hub",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state for search status
if 'search_complete' not in st.session_state:
    st.session_state.search_complete = False

# Initialize session state for preferences
if 'auto_play' not in st.session_state:
    st.session_state.auto_play = False
if 'show_descriptions' not in st.session_state:
    st.session_state.show_descriptions = False
if 'max_results' not in st.session_state:
    st.session_state.max_results = 6

# Initialize session state for video detail page
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'search'
if 'selected_video' not in st.session_state:
    st.session_state.selected_video = None
if 'video_summary' not in st.session_state:
    st.session_state.video_summary = None

# Initialize YouTube agent and Gemini agent
youtube_agent = YouTubeSearchAgent()
try:
    gemini_agent = GeminiSummaryAgent()
    gemini_available = True
except Exception as e:
    st.warning(f"Gemini API not available: {e}")
    gemini_available = False

# Configuration variables
# max_results = 5  # Number of videos to display
# auto_play = False  # Auto-play setting for videos
# show_descriptions = True  # Show full video descriptions

# Modern, vibrant, readable global CSS
st.markdown('''
<style>
:root {
  --primary: #00ffc3;
  --primary-dark: #00bfae;
  --accent: #ff6b81;
  --bg: #f6f8fa;
  --bg-glass: rgba(255,255,255,0.95);
  --header-bg: linear-gradient(90deg, #00ffc3 0%, #00bfae 100%);
  --footer-bg: linear-gradient(90deg, #232526 0%, #414345 100%);
  --text-main: #1a1a1a;
  --text-muted: #444;
  --shadow: 0 8px 32px rgba(0,0,0,0.10);
}
body, [data-testid="stAppViewContainer"] {
  background: var(--bg) !important;
  color: var(--text-main) !important;
  font-family: 'Inter', 'Segoe UI', Arial, sans-serif !important;
}
header[data-testid="stHeader"] {
  background: var(--header-bg) !important;
  border-bottom: 2px solid var(--primary-dark) !important;
  box-shadow: var(--shadow) !important;
  height: 64px !important;
}
.custom-header {
  position: sticky;
  top: 0;
  z-index: 1000;
  width: 100%;
  background: var(--header-bg);
  box-shadow: var(--shadow);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.2rem 2.5rem 1.2rem 2.5rem;
  border-radius: 0 0 18px 18px;
  margin-bottom: 2rem;
  backdrop-filter: blur(12px);
}
.header-logo {
  display: flex;
  align-items: center;
  gap: 0.7rem;
  font-weight: 900;
  font-size: 1.7rem;
  color: var(--primary-dark);
  text-decoration: none;
  letter-spacing: 1px;
  text-shadow: 0 2px 8px #fff;
}
.header-logo-icon {
  font-size: 2.2rem;
  filter: drop-shadow(0 2px 8px var(--primary));
}
.header-nav {
  display: flex;
  gap: 1.5rem;
}
.nav-link {
  color: var(--text-main);
  background: rgba(0,0,0,0.04);
  border-radius: 10px;
  padding: 0.7rem 1.5rem;
  font-weight: 700;
  font-size: 1.1rem;
  text-decoration: none;
  transition: background 0.2s, color 0.2s;
  border: 2px solid transparent;
  letter-spacing: 0.5px;
}
.nav-link:hover {
  background: var(--accent);
  color: #fff;
  border-color: var(--primary-dark);
}
.content-area {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1rem 0 1rem;
}
.video-grid-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 2rem;
  margin: 2rem 0;
}
.video-card {
  background: var(--bg-glass);
  border-radius: 18px;
  box-shadow: var(--shadow);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  transition: transform 0.2s, box-shadow 0.2s;
  border: 2px solid var(--primary-dark);
}
.video-card:hover {
  transform: translateY(-6px) scale(1.03);
  box-shadow: 0 12px 40px var(--primary-dark);
  border-color: var(--accent);
}
.video-thumbnail {
  width: 100%;
  height: 180px;
  object-fit: cover;
  border-radius: 18px 18px 0 0;
}
.video-content {
  padding: 1.5rem;
  flex: 1;
  display: flex;
  flex-direction: column;
}
.video-title {
  color: var(--primary-dark);
  font-size: 1.2rem;
  font-weight: 900;
  margin-bottom: 0.7rem;
  line-height: 1.3;
}
.video-channel {
  color: var(--accent);
  font-size: 1.05rem;
  margin-bottom: 0.7rem;
  font-weight: 700;
}
.video-description {
  color: var(--text-main);
  font-size: 1.05rem;
  margin-bottom: 1.1rem;
  flex: 1;
  font-weight: 600;
}
.video-actions {
  display: flex;
  gap: 0.7rem;
}
.watch-btn, .summary-btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  font-size: 1.1rem;
  font-weight: 800;
  border: none;
  border-radius: 12px;
  padding: 0.8rem 1.3rem;
  cursor: pointer;
  transition: background 0.2s, color 0.2s, box-shadow 0.2s;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  text-decoration: none;
  letter-spacing: 0.5px;
}
.watch-btn {
  background: linear-gradient(90deg, var(--primary), var(--primary-dark));
  color: #0a192f;
}
.watch-btn:hover {
  background: linear-gradient(90deg, var(--primary-dark), var(--primary));
  color: #fff;
}
.summary-btn {
  background: linear-gradient(90deg, var(--accent), #ffb86b);
  color: #fff;
}
.summary-btn:hover {
  background: linear-gradient(90deg, #ffb86b, var(--accent));
  color: #0a192f;
}
.suggestions-container {
  background: var(--bg-glass);
  border-radius: 15px;
  box-shadow: var(--shadow);
  margin: 2rem 0;
  padding: 2rem;
  border: 2px solid var(--primary-dark);
}
.suggestion-tag {
  display: inline-block;
  padding: 0.7rem 1.3rem;
  margin: 0.5rem;
  background: var(--primary-dark);
  border-radius: 25px;
  color: #fff;
  font-size: 1.05rem;
  cursor: pointer;
  transition: background 0.2s, color 0.2s;
  border: 2px solid var(--primary);
  font-weight: 700;
}
.suggestion-tag:hover {
  background: var(--accent);
  color: #fff;
  border-color: #fff;
}
.preferences-option {
  background: rgba(0,255,195,0.08);
  padding: 1rem 1.5rem;
  border-radius: 10px;
  margin: 0.5rem 0;
  border: 2px solid var(--primary-dark);
  transition: all 0.2s;
  font-weight: 700;
}
.preferences-option:hover {
  background: var(--primary-dark);
  color: #fff;
}
.footer {
  background: var(--footer-bg);
  color: #fff;
  padding: 2.5rem 1rem 1.5rem 1rem;
  border-radius: 18px 18px 0 0;
  margin-top: 3rem;
  text-align: center;
  box-shadow: var(--shadow);
}
.footer h3 {
  font-size: 2.2rem;
  font-weight: 900;
  margin-bottom: 0.7rem;
  background: linear-gradient(90deg, var(--primary), var(--accent));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.footer p {
  color: #fff;
  font-size: 1.15rem;
  margin: 0.5rem 0;
  font-weight: 700;
}
@media (max-width: 900px) {
  .content-area { padding: 1rem 0.2rem; }
  .video-grid-container { gap: 1rem; }
}
@media (max-width: 600px) {
  .custom-header { flex-direction: column; padding: 0.7rem 0.5rem; }
  .header-nav { gap: 0.5rem; }
  .content-area { padding: 0.5rem 0.1rem; }
  .video-card { padding: 1rem; }
  .footer { padding: 1.2rem 0.2rem; }
}
</style>
''', unsafe_allow_html=True)

def show_search_page():
    # Custom CSS for better styling
    st.markdown("""
    <style>
        /* Streamlit Header Adjustments */
        header[data-testid="stHeader"] {
            height: 60px !important;
            background: rgba(0, 12, 32, 0.98) !important;
            border-bottom: 1px solid rgba(0, 255, 204, 0.15) !important;
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            right: 0 !important;
            z-index: 999999 !important;
        }
        /* ... (all your CSS here, unchanged) ... */
    </style>
    """, unsafe_allow_html=True)

    # --- HEADER ---
    st.markdown("""
    <div class="custom-header" style="background: linear-gradient(90deg, #00ffc3 0%, #00bfae 50%, #ff6b81 100%); box-shadow: 0 4px 24px rgba(0,0,0,0.10); border-radius: 0 0 18px 18px;">
        <a href="#" class="header-logo" style="font-weight:900; color:#111; text-shadow:0 2px 8px #fff;">
            <span class="header-logo-icon">🎓</span>
            <span class="header-logo-text" style="color:#111; font-weight:900;">Video Learning Hub</span>
        </a>
        <nav class="header-nav">
            <a href="#search-section" class="nav-link" style="color:#fff; font-weight:800; text-shadow:0 2px 8px #222;">🔍 Search</a>
            <a href="#preferences-section" class="nav-link" style="color:#fff; font-weight:800; text-shadow:0 2px 8px #222;">⚙️ Settings</a>
        </nav>
    </div>
    """, unsafe_allow_html=True)

    # --- MAIN CONTENT AREA ---
    st.markdown('<div class="content-area">', unsafe_allow_html=True)
    
    # --- SEARCH SECTION ---
    st.markdown('<div id="search-section" class="desktop-only">', unsafe_allow_html=True)
    if st.session_state.get('mobile_drawer_open', False) is False:
        search_col1, search_col2 = st.columns([4, 1])
        with search_col1:
            query = st.text_input("What would you like to learn about today?", 
                                 placeholder="Enter any topic, question, or skill you want to learn...",
                                 key="search_input",
                                 label_visibility="visible")
        with search_col2:
            st.markdown('<div style="margin-top: 1.5rem;">', unsafe_allow_html=True)
            search_button = st.button("🔍 Explore", use_container_width=True, key="search_button")
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        query = st.session_state.get('mobile_query', '')
        search_button = st.session_state.get('mobile_search_button', False)

    # --- VIDEO GRID ---
    if query and search_button:
        try:
            st.session_state.search_complete = False
            with st.spinner(""):
                videos = youtube_agent.search_videos(
                    query, 
                    max_results=st.session_state.max_results
                )
                st.session_state.search_complete = True
                if videos:
                    st.markdown('<h2 style="color: #00ffcc; font-size: 2rem; font-weight: 700; margin: 2rem 0;">📺 Learning Resources</h2>', unsafe_allow_html=True)
                    st.markdown('<div class="video-grid-container">', unsafe_allow_html=True)
                    for video in videos:
                        short_desc = video['description'][:120] + '...' if len(video['description']) > 120 else video['description']
                        st.markdown(f"""
                            <div class="video-card">
                                <img src="https://img.youtube.com/vi/{video['video_id']}/hqdefault.jpg" 
                                     alt="{video['title']}" 
                                     class="video-thumbnail"
                                     onerror="this.src='https://via.placeholder.com/350x200/0a192f/00ffcc?text=Video+Thumbnail'">
                                <div class="video-content">
                                    <h3 class="video-title">{video['title']}</h3>
                                    <div class="video-channel">📺 {video['channel']}</div>
                                    <p class="video-description">{short_desc}</p>
                                    <div class="video-actions">
                                        <a href="{video['url']}" target="_blank" class="watch-btn">
                                            🎥 Watch on YouTube
                                        </a>
                                        <a href="?video_id={video['video_id']}&title={video['title'].replace('&', '%26').replace('"', '%22').replace("'", '%27').replace('<', '%3C').replace('>', '%3E')}&channel={video['channel'].replace('&', '%26').replace('"', '%22').replace("'", '%27').replace('<', '%3C').replace('>', '%3E')}&description={video['description'].replace('&', '%26').replace('"', '%22').replace("'", '%27').replace('<', '%3C').replace('>', '%3E')}" class="summary-btn">
                                            📋 AI Summary
                                        </a>
                                    </div>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.error("No videos found for your query. Please try different keywords.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.info("Please try again with a different search term or check your internet connection.")
    st.markdown('</div>', unsafe_allow_html=True)  # Close search section

    # --- SUGGESTIONS ---
    st.markdown('<div class="suggestions-container" style="margin: 2rem 0; padding: 2.5rem; background: rgba(17, 34, 64, 0.9); border-radius: 15px; border: 1px solid rgba(0, 255, 204, 0.1); box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);">', unsafe_allow_html=True)
    st.markdown("<h3 style='color: #64ffda; margin-bottom: 2rem; text-align: center; font-size: 1.8rem; font-weight: 700;'>Popular Topics</h3>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        st.markdown("""
            <div style="text-align: center; padding: 1rem;">
                <h4 style='color: #64ffda; margin-bottom: 1rem; font-size: 1.2rem; font-weight: 600;'>🔬 Science & Math</h4>
                <div class="suggestion-tag" style="margin: 0.5rem 0; display: block; text-align: center;">Quantum Physics</div>
                <div class="suggestion-tag" style="margin: 0.5rem 0; display: block; text-align: center;">Calculus Basics</div>
                <div class="suggestion-tag" style="margin: 0.5rem 0; display: block; text-align: center;">Chemistry Lab</div>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
            <div style="text-align: center; padding: 1rem;">
                <h4 style='color: #64ffda; margin-bottom: 1rem; font-size: 1.2rem; font-weight: 600;'>💻 Technology</h4>
                <div class="suggestion-tag" style="margin: 0.5rem 0; display: block; text-align: center;">Python Programming</div>
                <div class="suggestion-tag" style="margin: 0.5rem 0; display: block; text-align: center;">Web Development</div>
                <div class="suggestion-tag" style="margin: 0.5rem 0; display: block; text-align: center;">AI & Machine Learning</div>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
            <div style="text-align: center; padding: 1rem;">
                <h4 style='color: #64ffda; margin-bottom: 1rem; font-size: 1.2rem; font-weight: 600;'>📚 General Education</h4>
                <div class="suggestion-tag" style="margin: 0.5rem 0; display: block; text-align: center;">World History</div>
                <div class="suggestion-tag" style="margin: 0.5rem 0; display: block; text-align: center;">Literature</div>
                <div class="suggestion-tag" style="margin: 0.5rem 0; display: block; text-align: center;">Study Skills</div>
            </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # --- PREFERENCES ---
    st.markdown('<div id="preferences-section" class="desktop-only">', unsafe_allow_html=True)
    st.markdown('<div class="suggestions-container" style="margin: 2rem 0; padding: 2.5rem; background: rgba(17, 34, 64, 0.9); border-radius: 15px; border: 1px solid rgba(0, 255, 204, 0.1); box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);">', unsafe_allow_html=True)
    st.markdown("<h3 style='color: #00ffcc; margin-bottom: 2rem; text-align: center; font-size: 1.8rem; font-weight: 700;'>⚙️ Search Preferences</h3>", unsafe_allow_html=True)
    if st.session_state.get('mobile_drawer_open', False) is False:
        st.markdown('<div class="preferences-option" style="margin-bottom: 2rem;">', unsafe_allow_html=True)
        st.markdown('<p class="preference-label" style="text-align: center; margin-bottom: 1rem;">Number of Results</p>', unsafe_allow_html=True)
        new_max_results = st.slider("", 2, 12, st.session_state.max_results, label_visibility="collapsed", key="max_results_slider")
        if new_max_results != st.session_state.max_results:
            st.session_state.max_results = new_max_results
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.session_state.max_results = st.session_state.get('mobile_max_results', 6)
    if st.session_state.get('mobile_drawer_open', False) is False:
        st.markdown('<div class="preferences-option">', unsafe_allow_html=True)
        st.markdown('<p class="preference-label" style="text-align: center; margin-bottom: 1.5rem;">Playback Options</p>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            auto_play_new = st.checkbox("🎬 Enable Autoplay", value=st.session_state.auto_play, key="autoplay_checkbox")
            if auto_play_new != st.session_state.auto_play:
                st.session_state.auto_play = auto_play_new
        with col2:
            show_desc_new = st.checkbox("📝 Show Full Descriptions", value=st.session_state.show_descriptions, key="desc_checkbox")
            if show_desc_new != st.session_state.show_descriptions:
                st.session_state.show_descriptions = show_desc_new
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.session_state.auto_play = st.session_state.get('mobile_auto_play', False)
        st.session_state.show_descriptions = st.session_state.get('mobile_show_descriptions', False)
    st.markdown('</div></div>', unsafe_allow_html=True)

    # --- FOOTER ---
    st.markdown("""
    <div class="footer" style="background: linear-gradient(90deg, #232526 0%, #00ffc3 60%, #ff6b81 100%); color: #fff; border-radius: 18px 18px 0 0; margin-top: 3rem; text-align: center; box-shadow: 0 4px 24px rgba(0,0,0,0.10);">
        <h3 id="video-learning-hub" style="font-size:2.2rem; font-weight:900; margin-bottom:0.7rem; color:#111;">🎥 Video Learning Hub</h3>
        <p style="color:#fff; font-size:1.15rem; margin:0.5rem 0; font-weight:800; text-shadow:0 2px 8px #222;">Your gateway to educational content from YouTube</p>
        <p style="font-size: 1rem; color: #fff; margin-top: 1rem; font-weight:800; text-shadow:0 2px 8px #222;">
            © 2025 <b>AMEER HAMZA</b> / ameerhamzaconsulting@gmail.com
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)  # Close content area

# Main Application Logic
def main():
    # Check for video detail parameters in URL or session state
    video_id = st.query_params.get("video_id", None)
    video_title = st.query_params.get("title", None)
    video_channel = st.query_params.get("channel", None)
    video_description = st.query_params.get("description", None)
    
    # If video detail parameters are present, show video detail page
    if video_id and video_title and video_channel and video_description:
        show_video_detail_page(video_id, video_title, video_channel, video_description)
    else:
        show_search_page()

def show_video_detail_page(video_id, video_title, video_channel, video_description):
    """Display the video detail page with video player and AI-generated summary"""
    # Modern, vibrant, readable CSS for the AI summary page
    st.markdown('''
    <style>
    :root {
      --primary: #00ffc3;
      --primary-dark: #00bfae;
      --accent: #ff6b81;
      --bg: #f6f8fa;
      --bg-glass: rgba(255,255,255,0.95);
      --header-bg: linear-gradient(90deg, #00ffc3 0%, #00bfae 100%);
      --footer-bg: linear-gradient(90deg, #232526 0%, #414345 100%);
      --text-main: #1a1a1a;
      --text-muted: #444;
      --shadow: 0 8px 32px rgba(0,0,0,0.10);
    }
    body, [data-testid="stAppViewContainer"] {
      background: var(--bg) !important;
      color: var(--text-main) !important;
      font-family: 'Inter', 'Segoe UI', Arial, sans-serif !important;
    }
    .custom-header {
      position: sticky;
      top: 0;
      z-index: 1000;
      width: 100%;
      background: var(--header-bg);
      box-shadow: var(--shadow);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 1.2rem 2.5rem 1.2rem 2.5rem;
      border-radius: 0 0 18px 18px;
      margin-bottom: 2rem;
      backdrop-filter: blur(12px);
    }
    .header-logo {
      display: flex;
      align-items: center;
      gap: 0.7rem;
      font-weight: 900;
      font-size: 1.7rem;
      color: var(--primary-dark);
      text-decoration: none;
      letter-spacing: 1px;
      text-shadow: 0 2px 8px #fff;
    }
    .header-logo-icon {
      font-size: 2.2rem;
      filter: drop-shadow(0 2px 8px var(--primary));
    }
    .header-nav {
      display: flex;
      gap: 1.5rem;
    }
    .nav-link {
      color: var(--text-main);
      background: rgba(0,0,0,0.04);
      border-radius: 10px;
      padding: 0.7rem 1.5rem;
      font-weight: 700;
      font-size: 1.1rem;
      text-decoration: none;
      transition: background 0.2s, color 0.2s;
      border: 2px solid transparent;
      letter-spacing: 0.5px;
    }
    .nav-link:hover {
      background: var(--accent);
      color: #fff;
      border-color: var(--primary-dark);
    }
    .video-detail-page {
      max-width: 1200px;
      margin: 0 auto;
      padding: 2rem 1rem;
    }
    .video-detail-header {
      background: var(--bg-glass);
      padding: 2rem;
      border-radius: 16px;
      border: 2px solid var(--primary-dark);
      margin-bottom: 2rem;
      box-shadow: var(--shadow);
    }
    .video-detail-title {
      color: var(--primary-dark);
      font-size: 2.2rem;
      font-weight: 900;
      margin-bottom: 1rem;
      line-height: 1.3;
    }
    .video-detail-channel {
      color: var(--accent);
      font-size: 1.1rem;
      font-weight: 700;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }
    .video-detail-layout {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 2rem;
      margin-top: 2rem;
    }
    .video-player-container {
      background: var(--bg-glass);
      border-radius: 16px;
      padding: 1.5rem;
      border: 2px solid var(--primary-dark);
      box-shadow: var(--shadow);
    }
    .video-player-frame {
      width: 100%;
      height: 400px;
      border-radius: 12px;
      border: none;
      box-shadow: 0 8px 32px rgba(0, 0, 0, 0.13);
    }
    .summary-container {
      background: var(--bg-glass);
      border-radius: 16px;
      padding: 1.5rem;
      border: 2px solid var(--accent);
      box-shadow: var(--shadow);
      max-height: 500px;
      overflow-y: auto;
    }
    .summary-title {
      color: var(--accent);
      font-size: 1.5rem;
      font-weight: 900;
      margin-bottom: 1rem;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }
    .summary-content {
      color: var(--text-main);
      line-height: 1.6;
      font-size: 1.05rem;
      font-weight: 700;
    }
    .summary-content h1, .summary-content h2, .summary-content h3, .summary-content h4 {
      color: var(--accent);
      margin-top: 1.5rem;
      margin-bottom: 0.5rem;
    }
    .summary-content ul, .summary-content ol {
      margin-left: 1.5rem;
      margin-bottom: 1rem;
    }
    .summary-content li {
      margin-bottom: 0.5rem;
    }
    .summary-content strong {
      color: var(--primary-dark);
    }
    .video-info-section {
      background: var(--bg-glass);
      border-radius: 16px;
      padding: 1.5rem;
      border: 2px solid var(--primary-dark);
      margin-top: 2rem;
      box-shadow: var(--shadow);
    }
    .video-info-title {
      color: var(--primary-dark);
      font-size: 1.3rem;
      font-weight: 900;
      margin-bottom: 1rem;
    }
    .video-info-content {
      color: var(--text-main);
      line-height: 1.6;
      font-weight: 700;
    }
    .video-info-content strong {
      color: var(--primary-dark);
    }
    .youtube-link {
      background: linear-gradient(90deg, var(--accent), #ffb86b);
      color: #fff;
      padding: 0.85rem 1.7rem;
      border-radius: 12px;
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      gap: 0.5rem;
      font-weight: 900;
      margin-top: 1rem;
      font-size: 1.1rem;
      border: none;
      box-shadow: 0 2px 8px rgba(0,0,0,0.08);
      transition: background 0.2s, color 0.2s;
    }
    .youtube-link:hover {
      background: linear-gradient(90deg, #ffb86b, var(--accent));
      color: var(--primary-dark);
      text-decoration: none;
    }
    .footer {
      background: var(--footer-bg);
      color: #fff;
      padding: 2.5rem 1rem 1.5rem 1rem;
      border-radius: 18px 18px 0 0;
      margin-top: 3rem;
      text-align: center;
      box-shadow: var(--shadow);
    }
    .footer h3 {
      font-size: 2.2rem;
      font-weight: 900;
      margin-bottom: 0.7rem;
      background: linear-gradient(90deg, var(--primary), var(--accent));
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .footer p {
      color: #fff;
      font-size: 1.15rem;
      margin: 0.5rem 0;
      font-weight: 700;
    }
    @media (max-width: 900px) {
      .video-detail-page { padding: 1rem 0.2rem; }
      .video-detail-layout { gap: 1rem; }
    }
    @media (max-width: 600px) {
      .custom-header { flex-direction: column; padding: 0.7rem 0.5rem; }
      .header-nav { gap: 0.5rem; }
      .video-detail-page { padding: 0.5rem 0.1rem; }
      .video-info-section { padding: 1rem; }
      .footer { padding: 1.2rem 0.2rem; }
    }
    </style>
    ''', unsafe_allow_html=True)

    # --- HEADER ---
    st.markdown("""
    <div class="custom-header" style="background: linear-gradient(90deg, #00ffc3 0%, #00bfae 50%, #ff6b81 100%); box-shadow: 0 4px 24px rgba(0,0,0,0.10); border-radius: 0 0 18px 18px;">
        <a href="#" class="header-logo" style="font-weight:900; color:#111; text-shadow:0 2px 8px #fff;">
            <span class="header-logo-icon">🎓</span>
            <span class="header-logo-text" style="color:#111; font-weight:900;">Video Learning Hub</span>
        </a>
        <nav class="header-nav">
            <a href="#" class="nav-link" style="color:#fff; font-weight:800; text-shadow:0 2px 8px #222;">🏠 Home</a>
            <a href="#" class="nav-link" style="color:#fff; font-weight:800; text-shadow:0 2px 8px #222;">🔍 Search</a>
        </nav>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="video-detail-page">', unsafe_allow_html=True)
    
    # Header section
    st.markdown(f"""
        <div class="video-detail-header">
            <h1 class="video-detail-title">{video_title}</h1>
            <div class="video-detail-channel">📺 {video_channel}</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Main layout - Video player and Summary side by side
    st.markdown('<div class="video-detail-layout">', unsafe_allow_html=True)
    
    # Left side - Video Player
    st.markdown(f"""
        <div class="video-player-container">
            <iframe
                src="https://www.youtube.com/embed/{video_id}?autoplay={1 if st.session_state.auto_play else 0}&rel=0"
                frameborder="0"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowfullscreen
                class="video-player-frame"
            ></iframe>
        </div>
    """, unsafe_allow_html=True)
    
    # Right side - AI Summary
    st.markdown('<div class="summary-container">', unsafe_allow_html=True)
    st.markdown('<h2 class="summary-title">🤖 AI-Generated Summary</h2>', unsafe_allow_html=True)
    
    # Generate summary using Gemini API
    if gemini_available:
        with st.spinner("🤖 Generating AI summary..."):
            try:
                summary = gemini_agent.generate_video_summary(
                    video_title, 
                    video_description, 
                    video_channel
                )
                
                # Display the summary
                st.markdown(f"""
                    <div class="summary-content">
                        {summary}
                    </div>
                """, unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Error generating summary: {str(e)}")
                st.markdown(f"""
                    <div class="summary-content">
                        <h4>Summary Generation Failed</h4>
                        <p>Unable to generate AI summary at this time. Here's the video description:</p>
                        <p>{video_description}</p>
                    </div>
                """, unsafe_allow_html=True)
    else:
        st.warning("Gemini API is not available. Please check your API key configuration.")
        st.markdown(f"""
            <div class="summary-content">
                <h4>Video Description</h4>
                <p>{video_description}</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close summary container
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close video detail layout
    
    # Additional video information section
    st.markdown(f"""
        <div class="video-info-section">
            <h3 class="video-info-title">📋 Video Information</h3>
            <div class="video-info-content">
                <p><strong>Title:</strong> {video_title}</p>
                <p><strong>Channel:</strong> {video_channel}</p>
                <p><strong>Description:</strong> {video_description}</p>
                <a href="https://www.youtube.com/watch?v={video_id}" target="_blank" class="youtube-link">
                    🎥 Watch on YouTube
                </a>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # --- FOOTER ---
    st.markdown("""
    <div class="footer" style="background: linear-gradient(90deg, #232526 0%, #00ffc3 60%, #ff6b81 100%); color: #fff; border-radius: 18px 18px 0 0; margin-top: 3rem; text-align: center; box-shadow: 0 4px 24px rgba(0,0,0,0.10);">
        <h3 id="video-learning-hub" style="font-size:2.2rem; font-weight:900; margin-bottom:0.7rem; color:#111;">🎥 Video Learning Hub</h3>
        <p style="color:#fff; font-size:1.15rem; margin:0.5rem 0; font-weight:800; text-shadow:0 2px 8px #222;">Your gateway to educational content from YouTube</p>
        <p style="font-size: 1rem; color: #fff; margin-top: 1rem; font-weight:800; text-shadow:0 2px 8px #222;">
            © 2025 <b>AMEER HAMZA</b> / ameerhamzaconsulting@gmail.com
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)  # Close video detail page

# Run the main application
if __name__ == "__main__":
    main() 