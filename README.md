# YouTube Search Agent

A Python-based YouTube search agent that helps you find videos with detailed information using the YouTube Data API.

## Features

- Search for YouTube videos with detailed results
- Get video statistics (views, likes, comments)
- Clean command-line interface
- Detailed video descriptions
- Channel information

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Set up your YouTube API key:
   - Go to the [Google Cloud Console](https://console.cloud.google.com)
   - Create a new project or select an existing one
   - Enable the YouTube Data API v3
   - Create credentials (API key)
   - Copy your API key

3. Create a `.env` file in the root directory with your YouTube API key:
```
YOUTUBE_API_KEY=your_youtube_api_key_here
```

## Usage

Run the search agent:
```bash
python youtube_search.py
```

- Enter your search query when prompted
- The agent will display:
  - Video titles
  - Channel names
  - Video URLs
  - Brief descriptions
  - View counts
  - Like counts
  - Comment counts
- Type 'quit' to exit the program

## Example Queries

- "Python programming tutorials"
- "Guitar lessons for beginners"
- "Cooking Italian pasta"
- "Machine learning projects"

## Note

The YouTube Data API has quotas and usage limits. Make sure to check your [Google Cloud Console](https://console.cloud.google.com) for your current quota usage. 