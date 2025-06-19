import streamlit as st
import os
from youtube_search import YouTubeSearchAgent
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

# Page configuration with custom theme
st.set_page_config(
    page_title="Video Learning Assistant",
    page_icon="🎥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
        /* Global Styles */
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #0a192f 0%, #112240 100%);
            color: #e6f1ff;
        }
        
        .main {
            padding: 2rem;
        }
        
        /* Header Styles */
        .header-container {
            background: rgba(17, 34, 64, 0.8);
            padding: 2rem;
            border-radius: 15px;
            margin-bottom: 2rem;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(100, 255, 218, 0.1);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        }
        
        .agent-title {
            background: linear-gradient(120deg, #64ffda 20%, #00ff9d 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 3.5rem !important;
            font-weight: 800 !important;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
            margin-bottom: 1rem;
            letter-spacing: -1px;
        }
        
        /* Search Box Styles */
        .stTextInput > div > div > input {
            font-size: 1.2rem;
            padding: 1.2rem;
            border-radius: 15px;
            background: rgba(17, 34, 64, 0.9);
            border: 2px solid rgba(100, 255, 218, 0.3);
            color: #e6f1ff !important;
            font-weight: 500;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #64ffda;
            box-shadow: 0 0 15px rgba(100, 255, 218, 0.2);
        }
        
        /* Video Player Container */
        .video-player-container {
            background: rgba(10, 25, 47, 0.7);
            padding: 1.5rem;
            border-radius: 15px;
            margin: 1rem 0;
            border: 1px solid rgba(100, 255, 218, 0.1);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
        }
        
        /* Video Card Styles */
        .video-card {
            background: rgba(17, 34, 64, 0.8);
            padding: 2rem;
            border-radius: 15px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(100, 255, 218, 0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            margin: 1.5rem 0;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
        }
        
        .video-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 30px rgba(100, 255, 218, 0.15);
            border-color: rgba(100, 255, 218, 0.3);
        }

        .video-card h3 {
            color: #64ffda !important;
            font-size: 1.5rem !important;
            font-weight: 700 !important;
            margin-bottom: 1rem !important;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
        }

        .video-card p {
            color: #e6f1ff !important;
            font-size: 1.1rem !important;
            line-height: 1.6 !important;
            font-weight: 500 !important;
            margin: 1rem 0 !important;
        }

        .video-card strong {
            color: #64ffda !important;
            font-weight: 700 !important;
        }
        
        /* Button Styles */
        .stButton > button {
            background: linear-gradient(45deg, #64ffda, #00ff9d);
            color: #0a192f;
            padding: 1rem 2rem;
            border-radius: 10px;
            border: none;
            font-weight: 700;
            font-size: 1.1rem;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .stButton > button:hover {
            background: linear-gradient(45deg, #00ff9d, #64ffda);
            box-shadow: 0 0 20px rgba(100, 255, 218, 0.3);
            transform: translateY(-2px);
        }
        
        /* Sidebar Styles */
        [data-testid="stSidebar"] {
            background: rgba(10, 25, 47, 0.95);
            backdrop-filter: blur(10px);
        }

        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h3 {
            color: #64ffda !important;
            font-weight: 700 !important;
            font-size: 1.3rem !important;
            margin-top: 2rem !important;
        }

        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
            color: #e6f1ff !important;
            font-weight: 500 !important;
            font-size: 1.1rem !important;
        }

        .sidebar .sidebar-content {
            background: rgba(10, 25, 47, 0.95);
        }
        
        /* Footer Styles */
        .footer {
            background: rgba(17, 34, 64, 0.8);
            padding: 2.5rem;
            border-radius: 15px;
            margin-top: 3rem;
            text-align: center;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(100, 255, 218, 0.1);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
        }
        
        .footer h3 {
            background: linear-gradient(120deg, #64ffda 20%, #00ff9d 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 2rem !important;
            font-weight: 700 !important;
            margin-bottom: 1rem !important;
        }

        .footer p {
            color: #e6f1ff !important;
            font-weight: 500 !important;
            font-size: 1.1rem !important;
            margin: 0.7rem 0 !important;
        }
        
        /* Loading Animation */
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.3; }
            100% { opacity: 1; }
        }
        
        .loading {
            animation: pulse 1.5s infinite;
            color: #64ffda;
            font-size: 1.2rem;
            font-weight: 600;
        }

        /* Headers and Text */
        h1, h2, h3 {
            color: #e6f1ff !important;
            font-weight: 700 !important;
        }

        p {
            color: #e6f1ff !important;
            font-weight: 500 !important;
        }

        /* Spinner */
        .stSpinner > div {
            border-top-color: #64ffda !important;
            border-left-color: #64ffda !important;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize YouTube Search Agent
youtube_agent = YouTubeSearchAgent()

# Header
st.markdown("""
    <div class="header-container">
        <h1 class="agent-title">🎥 Video Learning Hub</h1>
        <p style="font-size: 1.4rem; color: #e6f1ff; font-weight: 600; text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);">
            Discover and learn from the best educational content on YouTube
        </p>
    </div>
""", unsafe_allow_html=True)

# Sidebar with information
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/video-playlist.png", width=100)
    st.markdown('<h2 style="color: #64ffda; font-weight: 700; font-size: 2rem;">🎥 Learning Guide</h2>', unsafe_allow_html=True)
    st.markdown("""
    <h3 style="color: #64ffda; margin-top: 2rem;">Features:</h3>
    
    <p style="color: #e6f1ff; font-weight: 500; font-size: 1.1rem; margin: 0.5rem 0;">
    1. 🔍 Smart video search<br>
    2. 📺 Instant video playback<br>
    3. 📱 Mobile-friendly interface<br>
    4. 🎯 Curated content
    </p>
    """, unsafe_allow_html=True)
    
    # Settings
    st.markdown('<hr style="border-color: rgba(100, 255, 218, 0.1);">', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #64ffda;">⚙️ Preferences</h3>', unsafe_allow_html=True)
    max_results = st.slider("Number of videos", 2, 8, 4)
    auto_play = st.checkbox("Enable video autoplay", value=False)
    show_descriptions = st.checkbox("Show full descriptions", value=False)

# Main content area
search_col1, search_col2 = st.columns([4, 1])
with search_col1:
    query = st.text_input("What would you like to learn about today?", 
                         placeholder="Enter any topic, question, or skill you want to learn...",
                         key="search_input")
with search_col2:
    st.markdown("<br>", unsafe_allow_html=True)
    search_button = st.button("🔍 Explore", use_container_width=True)

if query and search_button:
    try:
        # Show thinking animation
        with st.spinner(""):
            st.markdown('<p class="loading">🔍 Searching for the best educational videos...</p>', unsafe_allow_html=True)
            time.sleep(1)  # Simulate loading
            
            # Search for videos
            videos = youtube_agent.search_videos(query, max_results=max_results)
            
            if videos:
                st.markdown('<h2 style="color: #64ffda; font-size: 2rem; font-weight: 700; margin: 2rem 0;">📺 Learning Resources</h2>', unsafe_allow_html=True)
                for video in videos:
                    st.markdown(f"""
                    <div class="video-card">
                        <h3>{video['title']}</h3>
                        <div class="video-player-container">
                            <iframe
                                width="100%"
                                height="400"
                                src="https://www.youtube.com/embed/{video['video_id']}?autoplay={1 if auto_play else 0}"
                                frameborder="0"
                                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                                allowfullscreen
                                style="border-radius: 10px;"
                            ></iframe>
                        </div>
                        <p><strong>Channel:</strong> {video['channel']}</p>
                        <p>{video['description'][:200] + '...' if not show_descriptions else video['description']}</p>
                        <a href="{video['url']}" target="_blank">
                            <div class="stButton">
                                <button>🔗 Watch on YouTube</button>
                            </div>
                        </a>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.error("No videos found for your query. Please try different keywords.")
                    
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.info("Please try again with a different search term or check your internet connection.")

# Footer
st.markdown("""
<div class="footer">
    <h3>🎥 Video Learning Hub</h3>
    <p style="font-size: 1.2rem; font-weight: 600;">Your gateway to educational content from YouTube</p>
    <p style="font-size: 1rem; color: rgba(230, 241, 255, 0.8); margin-top: 1rem;">
        Built with 💚 using Streamlit and YouTube API | © 2024
    </p>
</div>
""", unsafe_allow_html=True) 