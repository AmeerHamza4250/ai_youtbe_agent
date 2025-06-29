import streamlit as st
import os
from youtube_search import YouTubeSearchAgent
from dotenv import load_dotenv
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

# Initialize YouTube agent
youtube_agent = YouTubeSearchAgent()

# Configuration variables
# max_results = 5  # Number of videos to display
# auto_play = False  # Auto-play setting for videos
# show_descriptions = True  # Show full video descriptions

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

        /* Main Content Padding */
        .main .block-container {
            padding-top: 60px !important;
            max-width: 1400px !important;
            margin: 0 auto !important;
        }

        /* Custom Header */
        .custom-header {
            position: fixed !important;
            top: 60px !important;
            left: 0 !important;
            right: 0 !important;
            height: 70px !important;
            background: linear-gradient(135deg, rgba(0, 12, 32, 0.98) 0%, rgba(0, 20, 40, 0.98) 100%) !important;
            backdrop-filter: blur(10px) !important;
            -webkit-backdrop-filter: blur(10px) !important;
            border-bottom: 2px solid rgba(0, 255, 204, 0.15) !important;
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.2) !important;
            z-index: 999998 !important;
            display: flex !important;
            align-items: center !important;
            justify-content: space-between !important;
            padding: 0 1rem !important;
        }

        /* Logo and Navigation Styles */
        .header-logo {
            display: flex !important;
            align-items: center !important;
            gap: 0.5rem !important;
            text-decoration: none !important;
            transition: all 0.3s ease !important;
        }

        .header-logo-icon {
            font-size: 1.8rem !important;
            color: #00ffcc !important;
            display: inline-flex !important;
            align-items: center !important;
            justify-content: center !important;
        }

        .header-logo-text {
            color: #00ffcc !important;
            font-size: 1.2rem !important;
            font-weight: 700 !important;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3) !important;
            white-space: nowrap !important;
        }

        .header-nav {
            display: flex !important;
            gap: 1rem !important;
            align-items: center !important;
        }

        .nav-link {
            color: #ffffff !important;
            text-decoration: none !important;
            font-size: 0.9rem !important;
            font-weight: 500 !important;
            padding: 0.4rem 0.8rem !important;
            border-radius: 6px !important;
            transition: all 0.3s ease !important;
            background: rgba(0, 255, 204, 0.1) !important;
            border: 1px solid rgba(0, 255, 204, 0.2) !important;
            white-space: nowrap !important;
        }

        .nav-link:hover {
            background: rgba(0, 255, 204, 0.2) !important;
            transform: translateY(-2px) !important;
            border-color: #00ffcc !important;
            color: #00ffcc !important;
        }

        /* Mobile Responsive Styles */
        @media screen and (max-width: 768px) {
            .custom-header {
                padding: 0 0.5rem !important;
                height: auto !important;
                min-height: 60px !important;
                flex-wrap: wrap !important;
                justify-content: center !important;
                gap: 0.5rem !important;
                padding-top: 0.5rem !important;
                padding-bottom: 0.5rem !important;
            }

            .header-logo {
                margin-right: 0 !important;
            }

            .header-logo-text {
                font-size: 1rem !important;
            }

            .header-nav {
                gap: 0.5rem !important;
                flex-wrap: wrap !important;
                justify-content: center !important;
            }

            .nav-link {
                font-size: 0.8rem !important;
                padding: 0.3rem 0.6rem !important;
            }

            /* Adjust main content padding for mobile */
            .content-area {
                margin-top: 180px !important;  /* Increased for mobile to ensure visibility */
                padding: 1rem 0.5rem !important;
            }
            
            /* Improve mobile grid layout */
            .video-grid-container {
                grid-template-columns: 1fr !important;
                gap: 1.5rem !important;
                padding: 0 0.5rem !important;
            }
            
            /* Adjust suggestion tags for mobile */
            .suggestion-tag {
                font-size: 1rem !important;
                padding: 0.6rem 1rem !important;
                margin: 0.3rem 0 !important;
            }
            
            /* Improve preferences layout on mobile */
            .preferences-option {
                padding: 1rem !important;
                margin: 0.5rem 0 !important;
            }
        }
        
        @media screen and (max-width: 480px) {
            .content-area {
                margin-top: 200px !important;
                padding: 0.5rem !important;
            }
            
            .video-grid-container {
                gap: 1rem !important;
                padding: 0 0.25rem !important;
            }
            
            .suggestions-container {
                padding: 1.5rem !important;
                margin: 1rem 0 !important;
            }
            
            .suggestion-tag {
                font-size: 0.9rem !important;
                padding: 0.5rem 0.8rem !important;
            }
            
            .preferences-option {
                padding: 0.8rem !important;
            }
        }
        
        /* Fix column alignment issues */
        [data-testid="column"] {
            display: flex !important;
            align-items: stretch !important;
            padding: 0.5rem !important;
        }
        
        /* Ensure proper spacing between sections */
        .stMarkdown {
            margin-bottom: 0 !important;
        }
        
        /* Improve button alignment */
        .stButton {
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
        }
        
        /* Fix checkbox alignment */
        .stCheckbox > div {
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
        }
        
        /* Improve slider alignment */
        .stSlider {
            margin: 1rem 0 !important;
        }
        
        /* Ensure consistent spacing */
        .element-container {
            margin-bottom: 1rem !important;
        }

        /* Existing styles without scroll-related CSS */
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

        /* Main Content Padding */
        .main .block-container {
            padding-top: 60px !important;
            max-width: 1400px !important;
            margin: 0 auto !important;
        }

        /* Custom Header */
        .custom-header {
            position: fixed !important;
            top: 60px !important;
            left: 0 !important;
            right: 0 !important;
            height: 70px !important;
            background: linear-gradient(135deg, rgba(0, 12, 32, 0.98) 0%, rgba(0, 20, 40, 0.98) 100%) !important;
            backdrop-filter: blur(10px) !important;
            -webkit-backdrop-filter: blur(10px) !important;
            border-bottom: 2px solid rgba(0, 255, 204, 0.15) !important;
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.2) !important;
            z-index: 999998 !important;
            display: flex !important;
            align-items: center !important;
            justify-content: space-between !important;
            padding: 0 2rem !important;
        }

        .header-logo {
            display: flex !important;
            align-items: center !important;
            gap: 1rem !important;
            text-decoration: none !important;
            transition: all 0.3s ease !important;
        }

        .header-logo-icon {
            font-size: 2rem !important;
            color: #00ffcc !important;
        }

        .header-logo-text {
            color: #00ffcc !important;
            font-size: 1.5rem !important;
            font-weight: 700 !important;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3) !important;
        }

        .header-nav {
            display: flex !important;
            gap: 2rem !important;
            align-items: center !important;
        }

        .nav-link {
            color: #ffffff !important;
            text-decoration: none !important;
            font-size: 1.1rem !important;
            font-weight: 500 !important;
            padding: 0.5rem 1rem !important;
            border-radius: 8px !important;
            transition: all 0.3s ease !important;
            background: rgba(0, 255, 204, 0.1) !important;
            border: 1px solid rgba(0, 255, 204, 0.2) !important;
        }

        .nav-link:hover {
            background: rgba(0, 255, 204, 0.2) !important;
            transform: translateY(-2px) !important;
            border-color: #00ffcc !important;
            color: #00ffcc !important;
            box-shadow: 0 4px 12px rgba(0, 255, 204, 0.2) !important;
        }

        /* Content Area */
        .content-area {
            margin-top: 160px !important;  /* Increased from 130px to add more space */
            padding: 2rem 1rem !important;
        }

        /* Hide hamburger menu */
        #MainMenu {
            visibility: visible !important;
        }

        /* Hide Streamlit footer */
        footer {
            visibility: hidden;
        }

        /* Streamlit Native Header Customization */
        header[data-testid="stHeader"] {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            height: 60px !important;
            background: rgba(0, 12, 32, 0.98) !important;
            backdrop-filter: blur(10px) !important;
            -webkit-backdrop-filter: blur(10px) !important;
            border-bottom: 1px solid rgba(0, 255, 204, 0.15) !important;
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.2) !important;
            z-index: 999999 !important;
            display: flex !important;
            align-items: center !important;
        }

        [data-testid="stToolbar"] {
            position: fixed !important;
            top: 0 !important;
            right: 0 !important;
            height: 80px !important;
            background: transparent !important;
            z-index: 999999 !important;
            display: flex !important;
            align-items: center !important;
            padding-right: 1rem !important;
        }

        /* Deploy Button Styling */
        .stDeployButton {
            visibility: visible !important;
            position: relative !important;
            z-index: 999999 !important;
        }

        [data-testid="stDeployButton"] button {
            background: rgba(0, 255, 204, 0.1) !important;
            border: 1px solid rgba(0, 255, 204, 0.2) !important;
            color: #00ffcc !important;
            border-radius: 12px !important;
            padding: 0.5rem 1.5rem !important;
            font-weight: 600 !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }

        [data-testid="stDeployButton"] button:hover {
            background: rgba(0, 255, 204, 0.15) !important;
            border-color: rgba(0, 255, 204, 0.3) !important;
            transform: translateY(-2px);
            box-shadow: 0 6px 15px rgba(0, 255, 204, 0.15) !important;
        }

        [data-testid="stDeployButton"] button span {
            color: #00ffcc !important;
            font-size: 1rem !important;
            letter-spacing: 0.5px !important;
        }

        /* Menu Button Styling */
        .stMainMenu button {
            visibility: visible !important;
            position: relative !important;
            z-index: 999999 !important;
            background: rgba(0, 255, 204, 0.08) !important;
            border: 1px solid rgba(0, 255, 204, 0.15) !important;
            border-radius: 10px !important;
            padding: 0.5rem !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            margin-left: 1rem !important;
        }

        .stMainMenu button:hover {
            background: rgba(0, 255, 204, 0.15) !important;
            border-color: rgba(0, 255, 204, 0.3) !important;
            transform: translateY(-2px);
            box-shadow: 0 6px 15px rgba(0, 255, 204, 0.15) !important;
        }

        .stMainMenu button svg {
            fill: #00ffcc !important;
        }

        /* Main Content */
        .main .block-container {
            padding-top: 130px !important;
            max-width: 1400px !important;
            margin: 0 auto !important;
        }

        /* Modern Fixed Header */
        .fixed-header {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            height: 75px;
            background: linear-gradient(135deg, rgba(0, 12, 32, 0.95) 0%, rgba(0, 20, 40, 0.95) 100%);
            backdrop-filter: blur(15px);
            -webkit-backdrop-filter: blur(15px);
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 2.5rem;
            z-index: 1000;
            border-bottom: 2px solid rgba(0, 255, 204, 0.15);
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.2);
        }

        /* Logo Container */
        .header-logo {
            display: flex;
            align-items: center;
            gap: 1rem;
            text-decoration: none;
            padding: 0.7rem 1.2rem;
            background: rgba(0, 255, 204, 0.08);
            border-radius: 16px;
            border: 1px solid rgba(0, 255, 204, 0.12);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .header-logo:hover {
            transform: translateY(-2px);
            background: rgba(0, 255, 204, 0.12);
            border-color: rgba(0, 255, 204, 0.25);
            box-shadow: 0 8px 20px rgba(0, 255, 204, 0.15);
        }

        .header-logo-icon {
            font-size: 2.2rem;
            filter: drop-shadow(0 2px 8px rgba(0, 255, 204, 0.3));
        }

        .header-logo-text {
            color: #00ffcc;
            font-size: 1.6rem;
            font-weight: 700;
            letter-spacing: 0.5px;
            text-shadow: 0 2px 8px rgba(0, 255, 204, 0.3);
        }

        /* Navigation */
        .header-nav {
            display: flex;
            gap: 1rem;
            align-items: center;
            background: rgba(0, 255, 204, 0.05);
            padding: 0.5rem;
            border-radius: 14px;
            border: 1px solid rgba(0, 255, 204, 0.1);
        }

        .nav-link {
            color: #ffffff;
            text-decoration: none;
            font-size: 1.1rem;
            font-weight: 600;
            padding: 0.8rem 1.5rem;
            border-radius: 12px;
            background: rgba(0, 255, 204, 0.08);
            border: 1px solid rgba(0, 255, 204, 0.15);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            display: flex;
            align-items: center;
            gap: 0.6rem;
            letter-spacing: 0.3px;
            white-space: nowrap;
        }

        .nav-link:hover {
            background: rgba(0, 255, 204, 0.15);
            transform: translateY(-2px);
            border-color: rgba(0, 255, 204, 0.3);
            color: #00ffcc;
            box-shadow: 0 6px 15px rgba(0, 255, 204, 0.15);
        }

        .nav-icon {
            font-size: 1.2rem;
            opacity: 0.9;
        }

        /* Main Content */
        .main-content {
            padding-top: 95px;
            max-width: 1400px;
            margin: 0 auto;
            padding-left: 2rem;
            padding-right: 2rem;
        }

        /* Section Headers */
        .section-header {
            color: #00ffcc;
            font-size: 2rem;
            font-weight: 700;
            margin: 2.5rem 0;
            text-shadow: 0 2px 8px rgba(0, 255, 204, 0.2);
            text-align: center;
            padding: 1.2rem;
            background: rgba(0, 255, 204, 0.05);
            border-radius: 16px;
            border: 1px solid rgba(0, 255, 204, 0.1);
            letter-spacing: 0.5px;
        }

        /* Fixed Header */
        .fixed-header {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            height: 70px;
            background: rgba(10, 25, 47, 0.95);
            backdrop-filter: blur(10px);
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 2rem;
            z-index: 1000;
            border-bottom: 1px solid rgba(0, 255, 204, 0.1);
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
        }

        .header-logo {
            display: flex;
            align-items: center;
            gap: 1rem;
            text-decoration: none;
            transition: all 0.3s ease;
        }

        .header-logo:hover {
            transform: translateY(-2px);
        }

        .header-logo-icon {
            font-size: 2rem;
        }

        .header-logo-text {
            color: #00ffcc;
            font-size: 1.5rem;
            font-weight: 700;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }

        .header-nav {
            display: flex;
            gap: 2rem;
            align-items: center;
        }

        .nav-link {
            color: #ffffff;
            text-decoration: none;
            font-size: 1.1rem;
            font-weight: 500;
            padding: 0.5rem 1rem;
            border-radius: 8px;
            transition: all 0.3s ease;
            background: rgba(0, 255, 204, 0.1);
            border: 1px solid rgba(0, 255, 204, 0.2);
        }

        .nav-link:hover {
            background: rgba(0, 255, 204, 0.2);
            transform: translateY(-2px);
            border-color: #00ffcc;
            color: #00ffcc;
            box-shadow: 0 4px 12px rgba(0, 255, 204, 0.2);
        }

        /* Main Content Padding for Fixed Header */
        .main-content {
            padding-top: 90px;
        }

        /* Smooth Scrolling */
        html {
            scroll-behavior: smooth !important;
        }

        /* Section IDs */
        #search-section, #preferences-section {
            scroll-margin-top: 80px;
        }

        /* Global Styles */
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #0a192f 0%, #112240 100%);
            color: #ffffff;
        }
        
        .main {
            padding: 2rem;
        }
        
        /* Header Styles */
        .header-container {
            background: rgba(17, 34, 64, 0.9);
            padding: 2rem;
            border-radius: 15px;
            margin-bottom: 2rem;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        }
        
        .agent-title {
            margin-top: 1rem !important;
            color: #00ffcc !important;
            font-size: 2.5rem !important;
            font-weight: 700 !important;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3) !important;
        }

        .educational-logo {
            font-size: 4rem !important;
            margin-bottom: 0.5rem !important;
            color: #00ffcc !important;
            text-shadow: 2px 2px 8px rgba(0,255,204,0.3);
            display: block;
            line-height: 1;
        }

        /* Search Box Styles */
        .stTextInput > div {
            height: 100%;
        }

        .stTextInput > div > div {
            height: 100%;
        }

        .stTextInput > div > div > input {
            font-size: 1.1rem !important;
            height: 46px !important;
            min-height: 46px !important;
            padding: 0 1rem !important;
            border-radius: 12px !important;
            background: rgba(17, 34, 64, 0.9) !important;
            border: 2px solid rgba(0, 255, 204, 0.3) !important;
            color: #ffffff !important;
            font-weight: 500 !important;
            line-height: 46px !important;
            caret-color: #00ffcc !important;
        }

        .stTextInput > div > div > input:focus {
            border-color: #00ffcc !important;
            box-shadow: 0 0 20px rgba(0, 255, 204, 0.2) !important;
            background: rgba(17, 34, 64, 0.95) !important;
        }

        .stTextInput > div > div > input::selection {
            background: rgba(0, 255, 204, 0.3) !important;
            color: #ffffff !important;
        }

        .stTextInput > div > div > input::placeholder {
            color: rgba(255, 255, 255, 0.5) !important;
            opacity: 1 !important;
        }

        .stTextInput > label {
            color: #00ffcc !important;
            font-weight: 600 !important;
            font-size: 1.1rem !important;
            padding-bottom: 0.5rem !important;
            height: 24px !important;
            line-height: 24px !important;
            margin-bottom: 0 !important;
        }

        /* Search Button */
        .stButton > button {
            height: 46px !important;
            min-height: 46px !important;
            background: rgba(0, 255, 204, 0.1) !important;
            color: #00ffcc !important;
            border: 2px solid rgba(0, 255, 204, 0.2) !important;
            border-radius: 12px !important;
            padding: 0 2rem !important;
            font-size: 1.1rem !important;
            font-weight: 600 !important;
            transition: all 0.3s ease !important;
            width: 100% !important;
            line-height: 42px !important;
            margin-top: 0 !important;
        }

        .stButton > button:hover {
            background: rgba(0, 255, 204, 0.15) !important;
            border-color: #00ffcc !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 12px rgba(0, 255, 204, 0.2) !important;
        }

        /* Column Alignment */
        [data-testid="column"] {
            display: flex !important;
            align-items: flex-end !important;
            padding: 0 !important;
        }

        [data-testid="column"]:first-child {
            padding-right: 1rem !important;
        }

        /* Fix vertical alignment */
        .element-container, .stVerticalBlock {
            margin-bottom: 0 !important;
            padding-bottom: 0 !important;
        }

        /* Suggestions Box */
        .suggestions-container {
            background: rgba(17, 34, 64, 0.9);
            padding: 2rem;
            border-radius: 15px;
            margin: 1rem 0 2rem 0;
            border: 1px solid rgba(0, 255, 204, 0.1);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        }

        .suggestion-tag {
            display: inline-block;
            padding: 0.8rem 1.5rem;
            margin: 0.5rem;
            background: rgba(0, 255, 204, 0.1);
            border-radius: 25px;
            color: #ffffff;
            font-size: 1.1rem !important;
            cursor: pointer;
            transition: all 0.3s ease;
            border: 1px solid rgba(0, 255, 204, 0.2);
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2);
        }

        .suggestion-tag:hover {
            background: rgba(0, 255, 204, 0.2);
            transform: translateY(-2px);
            border-color: #00ffcc;
            box-shadow: 0 4px 15px rgba(0, 255, 204, 0.2);
        }
        
        /* Video Player Container */
        .video-player-container {
            background: rgba(10, 25, 47, 0.8);
            padding: 1.5rem;
            border-radius: 15px;
            margin: 1rem 0;
            border: 1px solid rgba(0, 255, 204, 0.1);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        }
        
        /* Video Card Styles */
        .video-card {
            background: rgba(17, 34, 64, 0.9);
            padding: 2rem;
            border-radius: 15px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(0, 255, 204, 0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            margin: 1.5rem 0;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        }
        
        .video-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 30px rgba(0, 255, 204, 0.15);
            border-color: rgba(0, 255, 204, 0.3);
        }
        
        .video-card h3 {
            color: #00ffcc !important;
            font-size: 1.6rem !important;
            font-weight: 700 !important;
            margin-bottom: 1rem !important;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
            line-height: 1.4 !important;
        }
        
        .video-card p {
            color: #ffffff !important;
            font-size: 1.2rem !important;
            line-height: 1.6 !important;
            font-weight: 500 !important;
            margin: 1rem 0 !important;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2);
        }
        
        .video-card strong {
            color: #00ffcc !important;
            font-weight: 700 !important;
        }
        
        /* Button Styles */
        .stButton > button {
            background: linear-gradient(45deg, #00ffcc, #00ff99);
            color: #0a192f;
            padding: 1rem 2rem;
            border-radius: 10px;
            border: none;
            font-weight: 700;
            font-size: 1.2rem;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 1px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        }
        
        .stButton > button:hover {
            background: linear-gradient(45deg, #00ff99, #00ffcc);
            box-shadow: 0 6px 25px rgba(0, 255, 204, 0.3);
            transform: translateY(-2px);
        }

        /* Slider and Checkbox Styles */
        .stSlider div[data-baseweb="slider"] {
            margin-top: 1rem;
            }

        .stSlider [data-testid="stTickBar"] {
            color: #ffffff !important;
            }
            
        .stSlider [data-testid="stTickBarMin"], 
        .stSlider [data-testid="stTickBarMax"] {
            color: #ffffff !important;
                font-size: 1rem !important;
        }

        /* Section Headers */
        h1, h2, h3, h4 {
            color: #ffffff !important;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
            margin-bottom: 1rem !important;
            }
            
        h3 {
            font-size: 1.8rem !important;
            font-weight: 700 !important;
            }
            
        h4 {
            font-size: 1.4rem !important;
            font-weight: 600 !important;
            color: #00ffcc !important;
        }

        /* Footer Styles */
        .footer {
            background: rgba(17, 34, 64, 0.9);
            padding: 3rem;
            border-radius: 15px;
            margin-top: 3rem;
            text-align: center;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(0, 255, 204, 0.1);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        }
        
        .footer h3 {
            background: linear-gradient(120deg, #00ffcc 20%, #00ff99 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 2.5rem !important;
            font-weight: 700 !important;
            margin-bottom: 1.5rem !important;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }

        .footer p {
            color: #ffffff !important;
            font-weight: 500 !important;
            font-size: 1.2rem !important;
            margin: 0.7rem 0 !important;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2);
        }
        
        /* Loading Animation */
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.3; }
            100% { opacity: 1; }
        }
        
        .loading {
            animation: pulse 1.5s infinite;
            color: #00ffcc;
            font-size: 1.4rem;
            font-weight: 600;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2);
        }

        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}

        /* Label text for inputs */
        .stMarkdown p, .stMarkdown span {
            color: #ffffff !important;
            font-size: 1.1rem !important;
            font-weight: 500 !important;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2);
        }

        /* Preferences Styling */
        .preferences-option {
            background: rgba(0, 255, 204, 0.1);
            padding: 1rem 1.5rem;
            border-radius: 10px;
            margin: 0.5rem 0;
            border: 1px solid rgba(0, 255, 204, 0.2);
            transition: all 0.3s ease;
        }

        .preferences-option:hover {
            background: rgba(0, 255, 204, 0.15);
            border-color: rgba(0, 255, 204, 0.3);
            transform: translateY(-2px);
        }

        /* Checkbox Styling */
        .stCheckbox {
            padding: 0.8rem 0;
        }

        .stCheckbox > div {
            padding: 1rem 1.5rem;
            background: rgba(0, 255, 204, 0.15);
            border-radius: 12px;
            transition: all 0.3s ease;
            border: 1px solid rgba(0, 255, 204, 0.3);
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
        }

        .stCheckbox > div:hover {
            background: rgba(0, 255, 204, 0.2);
            border-color: rgba(0, 255, 204, 0.5);
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0, 255, 204, 0.2);
        }

        .stCheckbox > div > label {
            color: #ffffff !important;
            font-size: 1.2rem !important;
            font-weight: 600 !important;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
            letter-spacing: 0.5px;
        }

        .stCheckbox > div > label > p {
            font-size: 1.2rem !important;
            color: #ffffff !important;
            margin: 0 !important;
        }

        /* Checkbox input styling */
        .stCheckbox input[type="checkbox"] {
            width: 20px !important;
            height: 20px !important;
        }

        .stCheckbox input[type="checkbox"]:checked {
            background-color: #00ffcc !important;
            border-color: #00ffcc !important;
        }

        .stCheckbox span[data-baseweb="checkbox"] {
            background-color: rgba(0, 255, 204, 0.2) !important;
            border-color: #00ffcc !important;
            width: 24px !important;
            height: 24px !important;
        }

        /* Search input styling */
        .stTextInput > div > div > input::placeholder {
            color: rgba(255, 255, 255, 0.7) !important;
        }

        /* Label styling */
        [data-testid="stWidgetLabel"] {
            color: #ffffff !important;
            font-size: 1.2rem !important;
            font-weight: 600 !important;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
            margin-bottom: 0.5rem !important;
        }

        [data-testid="stWidgetLabel"] p {
            color: #ffffff !important;
            font-size: 1.2rem !important;
            margin: 0 !important;
        }

        /* Slider Styling */
        .stSlider > div > div > div > div {
            background-color: #00ffcc !important;
        }

        .stSlider > div > div > div > div > div {
            background-color: #00ffcc !important;
            border-color: #00ffcc !important;
        }

        .stSlider > div > div > div[data-baseweb="thumb"] {
            background-color: #ffffff !important;
            border-color: #00ffcc !important;
        }

        .preference-label {
            color: #00ffcc !important;
            font-size: 1.2rem !important;
            font-weight: 600 !important;
            margin-bottom: 0.5rem !important;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2);
        }

        .desktop-only { display: inline-block !important; }
        .mobile-only { display: none !important; }
        @media screen and (max-width: 768px) {
            .desktop-only { display: none !important; }
            .mobile-only { display: block !important; }
            .hamburger {
                background: none;
                border: none;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                width: 40px;
                height: 40px;
                cursor: pointer;
                gap: 5px;
                margin-left: 0.5rem;
            }
            .hamburger span {
                display: block;
                width: 28px;
                height: 4px;
                background: #00ffcc;
                border-radius: 2px;
                transition: all 0.3s;
            }
        }
    </style>

    <script>
    function openMobileDrawer() {
        document.getElementById('mobile-drawer').style.right = '0';
        document.getElementById('mobile-drawer-overlay').style.display = 'block';
    }
    function closeMobileDrawer() {
        document.getElementById('mobile-drawer').style.right = '-100vw';
        document.getElementById('mobile-drawer-overlay').style.display = 'none';
    }
    </script>

    <!-- Custom Header -->
    <div class="custom-header">
        <a href="#" class="header-logo">
            <div class="header-logo-icon">🎓</div>
            <span class="header-logo-text">Video Learning Hub</span>
        </a>
        <nav class="header-nav">
            <a href="#search-section" class="nav-link desktop-only">🔍 Search</a>
            <a href="#preferences-section" class="nav-link desktop-only">⚙️ Preferences</a>
            <button class="hamburger mobile-only" aria-label="Open menu" onclick="openMobileDrawer()">
                <span></span><span></span><span></span>
            </button>
        </nav>
    </div>

    <!-- Mobile Drawer Overlay -->
    <div id="mobile-drawer-overlay" class="mobile-only" style="display:none;position:fixed;top:0;left:0;width:100vw;height:100vh;background:rgba(0,0,0,0.4);z-index:1000001;" onclick="closeMobileDrawer()"></div>
    <!-- Mobile Drawer Side Panel -->
    <div id="mobile-drawer" class="mobile-only" style="position:fixed;top:0;right:-100vw;width:85vw;max-width:400px;height:100vh;background:linear-gradient(135deg,#0a192f 0%,#112240 100%);z-index:1000002;transition:right 0.3s cubic-bezier(.4,0,.2,1);box-shadow:-4px 0 30px rgba(0,0,0,0.3);padding:2rem 1.5rem;overflow-y:auto;">
        <button style="background:none;border:none;position:absolute;top:1.2rem;right:1.2rem;font-size:2rem;color:#00ffcc;cursor:pointer;" aria-label="Close menu" onclick="closeMobileDrawer()">&times;</button>
        <div style="margin-top:2.5rem;">
            <div class="educational-logo" style="font-size:2.5rem;margin-bottom:1rem;">🎓</div>
            <h2 style="color:#00ffcc;font-size:1.5rem;font-weight:700;margin-bottom:2rem;">Menu</h2>
            <div id="mobile-search-section"></div>
            <div id="mobile-preferences-section"></div>
        </div>
    </div>

    <!-- Content Area -->
    <div class="content-area">
        <div style="text-align: center;">
            <div class="educational-logo" aria-label="Educational Logo" title="Educational Logo">🎓</div>
            <h1 class="agent-title">Video Learning Hub</h1>
            <div class="header-container">
                <p style="font-size: 1.4rem; color: #ffffff; font-weight: 600; text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3); text-align: center;">
                    Discover and learn from the best educational content on YouTube
                </p>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Search Section with ID
st.markdown('<div id="search-section" class="desktop-only">', unsafe_allow_html=True)

# Desktop search
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

# Handle search
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
                
                # Add CSS for proper video grid layout
                st.markdown("""
                <style>
                .video-grid-container {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
                    gap: 2rem;
                    margin: 2rem 0;
                    padding: 0 1rem;
                }
                
                .video-card {
                    background: rgba(17, 34, 64, 0.95);
                    border-radius: 16px;
                    overflow: hidden;
                    backdrop-filter: blur(15px);
                    border: 1px solid rgba(0, 255, 204, 0.15);
                    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
                    position: relative;
                    height: 500px;
                    display: flex;
                    flex-direction: column;
                }
                
                .video-card:hover {
                    transform: translateY(-8px) scale(1.02);
                    box-shadow: 0 20px 40px rgba(0, 255, 204, 0.2);
                    border-color: rgba(0, 255, 204, 0.4);
                }
                
                .video-thumbnail {
                    width: 100%;
                    height: 180px;
                    object-fit: cover;
                    border-radius: 16px 16px 0 0;
                    transition: transform 0.3s ease;
                }
                
                .video-card:hover .video-thumbnail {
                    transform: scale(1.05);
                }
                
                .video-content {
                    padding: 1.5rem;
                    flex: 1;
                    display: flex;
                    flex-direction: column;
                }
                
                .video-title {
                    color: #00ffcc !important;
                    font-size: 1.1rem !important;
                    font-weight: 700 !important;
                    margin-bottom: 0.75rem !important;
                    line-height: 1.4 !important;
                    display: -webkit-box;
                    -webkit-line-clamp: 2;
                    -webkit-box-orient: vertical;
                    overflow: hidden;
                    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
                    min-height: 2.8rem;
                }
                
                .video-channel {
                    color: #ffffff !important;
                    font-size: 0.85rem !important;
                    font-weight: 500 !important;
                    margin-bottom: 0.75rem !important;
                    opacity: 0.9;
                    display: flex;
                    align-items: center;
                    gap: 0.5rem;
                }
                
                .video-description {
                    color: rgba(255, 255, 255, 0.85) !important;
                    font-size: 0.8rem !important;
                    line-height: 1.5 !important;
                    margin-bottom: 1.25rem !important;
                    display: -webkit-box;
                    -webkit-line-clamp: 3;
                    -webkit-box-orient: vertical;
                    overflow: hidden;
                    flex: 1;
                }
                
                .video-actions {
                    margin-top: auto;
                    padding-top: 1rem;
                }
                
                .watch-btn {
                    background: linear-gradient(135deg, #00ffcc, #00ff99);
                    color: #0a192f !important;
                    padding: 0.75rem 1.25rem;
                    border-radius: 10px;
                    border: none;
                    font-weight: 600;
                    font-size: 0.85rem;
                    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                    text-decoration: none;
                    display: inline-flex;
                    align-items: center;
                    justify-content: center;
                    width: 100%;
                    text-transform: uppercase;
                    letter-spacing: 0.5px;
                    box-shadow: 0 4px 15px rgba(0, 255, 204, 0.2);
                    cursor: pointer;
                }
                
                .watch-btn:hover {
                    background: linear-gradient(135deg, #00ff99, #00ffcc);
                    transform: translateY(-2px);
                    box-shadow: 0 8px 25px rgba(0, 255, 204, 0.4);
                    color: #0a192f !important;
                    text-decoration: none;
                }
                
                /* Responsive Design */
                @media (max-width: 1200px) {
                    .video-grid-container {
                        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                        gap: 1.5rem;
                    }
                }
                
                @media (max-width: 768px) {
                    .video-grid-container {
                        grid-template-columns: 1fr;
                        gap: 1.5rem;
                        padding: 0 0.5rem;
                    }
                    
                    .video-card {
                        height: 450px;
                    }
                    
                    .video-thumbnail {
                        height: 160px;
                    }
                    
                    .video-content {
                        padding: 1.25rem;
                    }
                }
                
                @media (max-width: 480px) {
                    .video-grid-container {
                        gap: 1rem;
                    }
                    
                    .video-card {
                        height: 420px;
                    }
                    
                    .video-thumbnail {
                        height: 140px;
                    }
                    
                    .video-content {
                        padding: 1rem;
                    }
                    
                    .video-title {
                        font-size: 1rem !important;
                    }
                }
                </style>
                """, unsafe_allow_html=True)
                
                # Start video grid
                st.markdown('<div class="video-grid-container">', unsafe_allow_html=True)
                
                for video in videos:
                    # Truncate description for card view
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
                                </div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                
                # Close video grid
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.error("No videos found for your query. Please try different keywords.")
                
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.info("Please try again with a different search term or check your internet connection.")

st.markdown('</div>', unsafe_allow_html=True)  # Close search section

# Add spacing between search results and popular topics
st.markdown('<div style="margin: 4rem 0;"></div>', unsafe_allow_html=True)

# Educational Search Suggestions
st.markdown('<div class="suggestions-container" style="margin: 2rem 0; padding: 2.5rem; background: rgba(17, 34, 64, 0.9); border-radius: 15px; border: 1px solid rgba(0, 255, 204, 0.1); box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);">', unsafe_allow_html=True)
st.markdown("<h3 style='color: #64ffda; margin-bottom: 2rem; text-align: center; font-size: 1.8rem; font-weight: 700;'>Popular Topics</h3>", unsafe_allow_html=True)

# Create responsive columns for different subject areas
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

# Add spacing between popular topics and preferences
st.markdown('<div style="margin: 4rem 0;"></div>', unsafe_allow_html=True)

# Preferences Section with ID
st.markdown('<div id="preferences-section" class="desktop-only">', unsafe_allow_html=True)
st.markdown('<div class="suggestions-container" style="margin: 2rem 0; padding: 2.5rem; background: rgba(17, 34, 64, 0.9); border-radius: 15px; border: 1px solid rgba(0, 255, 204, 0.1); box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);">', unsafe_allow_html=True)
st.markdown("<h3 style='color: #00ffcc; margin-bottom: 2rem; text-align: center; font-size: 1.8rem; font-weight: 700;'>⚙️ Search Preferences</h3>", unsafe_allow_html=True)

# Number of videos slider
if st.session_state.get('mobile_drawer_open', False) is False:
    st.markdown('<div class="preferences-option" style="margin-bottom: 2rem;">', unsafe_allow_html=True)
    st.markdown('<p class="preference-label" style="text-align: center; margin-bottom: 1rem;">Number of Results</p>', unsafe_allow_html=True)
    new_max_results = st.slider("", 2, 12, st.session_state.max_results, label_visibility="collapsed", key="max_results_slider")
    if new_max_results != st.session_state.max_results:
        st.session_state.max_results = new_max_results
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.session_state.max_results = st.session_state.get('mobile_max_results', 6)

# Playback Options
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

# Add final spacing before footer
st.markdown('<div style="margin: 3rem 0;"></div>', unsafe_allow_html=True)

# Footer
st.markdown("""
    <div class="footer">
        <h3>🎥 Video Learning Hub</h3>
        <p style="font-size: 1.2rem; font-weight: 600;">Your gateway to educational content from YouTube</p>
        <p style="font-size: 1rem; color: rgba(230, 241, 255, 0.8); margin-top: 1rem;">
            © 2025 [AMEER HAMZA / ameerhamzaconsulting@gmail.com ]. All rights reserved.
        </p>
    </div>
""", unsafe_allow_html=True) 