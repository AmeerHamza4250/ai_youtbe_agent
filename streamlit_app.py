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

# Custom CSS for better styling
st.markdown("""
    <style>
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
            height: 80px !important;
            background: linear-gradient(135deg, rgba(0, 12, 32, 0.98) 0%, rgba(0, 20, 40, 0.98) 100%) !important;
            backdrop-filter: blur(10px) !important;
            -webkit-backdrop-filter: blur(10px) !important;
            border-bottom: 2px solid rgba(0, 255, 204, 0.15) !important;
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

        /* Add padding to main content to account for fixed header */
        .main .block-container {
            padding-top: 110px !important;
            max-width: 1400px !important;
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
            scroll-behavior: smooth;
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
            background: linear-gradient(120deg, #00ffcc 20%, #00ff99 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 4rem !important;
            font-weight: 800 !important;
            text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.4);
            margin-bottom: 1rem;
            letter-spacing: -1px;
            text-align: center;
            padding: 1rem 0;
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

        /* Mobile Responsive Styles */
        @media (max-width: 768px) {
            .main .block-container {
                padding-left: 0.5rem !important;
                padding-right: 0.5rem !important;
            }

            .stTextInput > div > div > input {
                font-size: 1rem !important;
                padding: 0 0.8rem !important;
            }

            .stButton > button {
                padding: 0 1rem !important;
                font-size: 1rem !important;
            }

            [data-testid="column"] {
                width: 100% !important;
                flex: 1 1 auto !important;
            }

            [data-testid="column"]:first-child {
                padding-right: 0 !important;
                margin-bottom: 0.5rem !important;
            }

            .video-card {
                padding: 1rem !important;
                margin-bottom: 1.5rem !important;
            }

            .video-card h3 {
                font-size: 1.1rem !important;
                line-height: 1.4 !important;
            }

            .video-player-container {
                position: relative !important;
                width: 100% !important;
                padding-bottom: 56.25% !important; /* 16:9 Aspect Ratio */
                height: 0 !important;
                margin: 1rem 0 !important;
            }

            .video-player-container iframe {
                position: absolute !important;
                top: 0 !important;
                left: 0 !important;
                width: 100% !important;
                height: 100% !important;
            }
        }

        /* Video Card Styles */
        .video-card {
            background: rgba(0, 12, 32, 0.5);
            border: 1px solid rgba(0, 255, 204, 0.2);
            border-radius: 16px;
            padding: 1.5rem;
            margin-bottom: 2rem;
            transition: all 0.3s ease;
        }

        .video-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
            border-color: rgba(0, 255, 204, 0.4);
        }

        .video-card h3 {
            color: #00ffcc;
            font-size: 1.3rem;
            font-weight: 600;
            margin-bottom: 1rem;
            line-height: 1.5;
        }

        .video-player-container {
            position: relative;
            width: 100%;
            padding-bottom: 56.25%; /* 16:9 Aspect Ratio */
            height: 0;
            margin: 1.5rem 0;
            border-radius: 12px;
            overflow: hidden;
        }

        .video-player-container iframe {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            border-radius: 12px;
        }
    </style>

    <!-- Modern Fixed Header -->
    <header class="fixed-header">
        <a href="#" class="header-logo">
            <span class="header-logo-icon">🎓</span>
            <span class="header-logo-text">Video Learning Hub</span>
        </a>
        <nav class="header-nav">
            <a href="#search-section" class="nav-link">
                <span class="nav-icon">🔍</span>
                Search
            </a>
            <a href="#preferences-section" class="nav-link">
                <span class="nav-icon">⚙️</span>
                Preferences
            </a>
        </nav>
    </header>

    <div class="main-content">
""", unsafe_allow_html=True)

# Title and Description
st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <div style="font-size: 5rem; margin-bottom: 1rem;">🎓</div>
        <h1 class="agent-title">Video Learning Hub</h1>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="header-container">
        <p style="font-size: 1.4rem; color: #ffffff; font-weight: 600; text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3); text-align: center;">
            Discover and learn from the best educational content on YouTube
        </p>
    </div>
""", unsafe_allow_html=True)

# Initialize YouTube Search Agent
youtube_agent = YouTubeSearchAgent()

# Initialize session state for search status
if 'search_complete' not in st.session_state:
    st.session_state.search_complete = False

# Search Section with ID
st.markdown('<div id="search-section">', unsafe_allow_html=True)

# Search bar with Explore button
search_col1, search_col2 = st.columns([4, 1])
with search_col1:
    query = st.text_input("What would you like to learn about today?", 
                         placeholder="Enter any topic, question, or skill you want to learn...",
                         key="search_input",
                         label_visibility="visible")
with search_col2:
    search_button = st.button("🔍 Explore", use_container_width=True)

# Educational Search Suggestions
st.markdown('<div class="suggestions-container">', unsafe_allow_html=True)
st.markdown("<h3 style='color: #64ffda; margin-bottom: 1rem;'>Popular Topics</h3>", unsafe_allow_html=True)

# Create columns for different subject areas
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <h4 style='color: #64ffda; margin-bottom: 0.5rem;'>Science & Math</h4>
        <div class="suggestion-tag">Quantum Physics</div>
        <div class="suggestion-tag">Calculus Basics</div>
        <div class="suggestion-tag">Chemistry Lab</div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <h4 style='color: #64ffda; margin-bottom: 0.5rem;'>Technology</h4>
        <div class="suggestion-tag">Python Programming</div>
        <div class="suggestion-tag">Web Development</div>
        <div class="suggestion-tag">AI & Machine Learning</div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <h4 style='color: #64ffda; margin-bottom: 0.5rem;'>General Education</h4>
        <div class="suggestion-tag">World History</div>
        <div class="suggestion-tag">Literature</div>
        <div class="suggestion-tag">Study Skills</div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Preferences Section with ID
st.markdown('<div id="preferences-section">', unsafe_allow_html=True)
st.markdown('<div class="suggestions-container">', unsafe_allow_html=True)
st.markdown("<h3 style='color: #00ffcc; margin-bottom: 1.5rem;'>Search Preferences</h3>", unsafe_allow_html=True)

# Number of videos slider
st.markdown('<div class="preferences-option">', unsafe_allow_html=True)
st.markdown('<p class="preference-label">Number of Results</p>', unsafe_allow_html=True)
max_results = st.slider("", 2, 8, 4, label_visibility="collapsed")
st.markdown('</div>', unsafe_allow_html=True)

# Playback Options
st.markdown('<div class="preferences-option">', unsafe_allow_html=True)
st.markdown('<p class="preference-label">Playback Options</p>', unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    auto_play = st.checkbox("Enable Autoplay", value=False)

with col2:
    show_descriptions = st.checkbox("Show Full Descriptions", value=False)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div></div>', unsafe_allow_html=True)

# Close main-content div
st.markdown('</div>', unsafe_allow_html=True)

# Handle search
if query and search_button:
    try:
        st.session_state.search_complete = False
        with st.spinner(""):
            if not st.session_state.search_complete:
                st.markdown('<p class="loading">🔍 Searching for the best educational videos...</p>', unsafe_allow_html=True)
            
            videos = youtube_agent.search_videos(
                query, 
                max_results=max_results
            )
            
            st.session_state.search_complete = True
            
            if videos:
                st.markdown('<h2 style="color: #00ffcc; font-size: 2rem; font-weight: 700; margin: 2rem 0;">📺 Learning Resources</h2>', unsafe_allow_html=True)
                
                for video in videos:
                    st.markdown(f"""
                        <div class="video-card">
                            <h3>{video['title']}</h3>
                            <div class="video-player-container">
                                <iframe
                                    src="https://www.youtube.com/embed/{video['video_id']}?autoplay={1 if auto_play else 0}"
                                    frameborder="0"
                                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                                    allowfullscreen
                                ></iframe>
                            </div>
                            <p><strong>Channel:</strong> {video['channel']}</p>
                            <p>{video['description'][:200] + '...' if not show_descriptions else video['description']}</p>
                            <a href="{video['url']}" target="_blank" class="watch-button">
                                <button style="
                                    background: rgba(0, 255, 204, 0.1);
                                    color: #00ffcc;
                                    border: 1px solid rgba(0, 255, 204, 0.3);
                                    padding: 0.5rem 1rem;
                                    border-radius: 8px;
                                    font-size: 1rem;
                                    cursor: pointer;
                                    transition: all 0.3s ease;
                                    margin-top: 1rem;
                                    width: 100%;
                                ">🔗 Watch on YouTube</button>
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
            © 2025 [AMEER HAMZA / ameerhamzaconsulting@gmail.com ]. All rights reserved.
        </p>
    </div>
""", unsafe_allow_html=True) 