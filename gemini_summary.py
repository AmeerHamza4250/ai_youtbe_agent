import os
import google.generativeai as genai
from dotenv import load_dotenv
import re

# Load environment variables
load_dotenv()

class GeminiSummaryAgent:
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('models/gemini-1.5-flash')

    def generate_video_summary(self, video_title, video_description, video_channel):
        """
        Generate a comprehensive summary of a video using Gemini API
        """
        try:
            prompt = f"""
            Please provide a comprehensive summary of this educational video:
            
            Title: {video_title}
            Channel: {video_channel}
            Description: {video_description}
            
            Please provide a structured summary that includes:
            1. **Main Topic**: What is the primary subject of this video?
            2. **Key Points**: What are the main concepts or lessons covered?
            3. **Learning Objectives**: What will viewers learn from this video?
            4. **Difficulty Level**: Is this beginner, intermediate, or advanced content?
            5. **Target Audience**: Who would benefit most from this video?
            6. **Practical Applications**: How can this knowledge be applied?
            7. **Related Topics**: What subjects are related to this content?
            
            Format the response in a clear, educational manner with proper headings and bullet points.
            Keep the summary concise but informative (around 300-400 words).
            """
            
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            print(f"Error generating summary: {e}")
            return f"""
            **Video Summary**
            
            **Title**: {video_title}
            **Channel**: {video_channel}
            
            **Description**: {video_description[:200]}...
            
            *Summary generation is currently unavailable. Please watch the video for detailed information.*
            """

    def generate_quick_summary(self, video_title, video_description):
        """
        Generate a quick, concise summary for video cards
        """
        try:
            prompt = f"""
            Provide a brief, engaging summary of this video in 2-3 sentences:
            
            Title: {video_title}
            Description: {video_description}
            
            Focus on the main learning outcome and why someone should watch this video.
            """
            
            response = self.model.generate_content(prompt)
            return response.text.strip()
            
        except Exception as e:
            print(f"Error generating quick summary: {e}")
            return f"Learn about {video_title.lower()} in this educational video."

    def extract_key_topics(self, video_title, video_description):
        """
        Extract key topics and tags from video content
        """
        try:
            prompt = f"""
            Extract 5-7 key topics or tags from this video content:
            
            Title: {video_title}
            Description: {video_description}
            
            Return only the topics as a comma-separated list, no additional text.
            """
            
            response = self.model.generate_content(prompt)
            topics = response.text.strip().split(',')
            return [topic.strip() for topic in topics if topic.strip()]
            
        except Exception as e:
            print(f"Error extracting topics: {e}")
            return ["Educational Content", "Learning", "Tutorial"]

    def generate_transcript_summary(self, video_title, video_channel, transcript):
        """
        Generate a comprehensive summary of a video using its transcript with Gemini API
        """
        try:
            prompt = f"""
            Please provide a comprehensive summary of this educational video based on its transcript.
            
            Title: {video_title}
            Channel: {video_channel}
            Transcript: {transcript[:4000]}
            
            Please provide a structured summary that includes:
            1. **Main Topic**: What is the primary subject of this video?
            2. **Key Points**: What are the main concepts or lessons covered?
            3. **Learning Objectives**: What will viewers learn from this video?
            4. **Difficulty Level**: Is this beginner, intermediate, or advanced content?
            5. **Target Audience**: Who would benefit most from this video?
            6. **Practical Applications**: How can this knowledge be applied?
            7. **Related Topics**: What subjects are related to this content?
            
            Format the response in a clear, educational manner with proper headings and bullet points.
            Keep the summary concise but informative (around 300-400 words).
            """
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error generating transcript summary: {e}")
            return f"*Summary generation from transcript is currently unavailable. Error: {e}*"

def main():
    # Test the Gemini integration
    agent = GeminiSummaryAgent()
    
    test_video = {
        'title': 'Introduction to Python Programming',
        'description': 'Learn the basics of Python programming language including variables, loops, and functions.',
        'channel': 'Programming Tutorials'
    }
    
    print("Testing Gemini Summary Generation...")
    summary = agent.generate_video_summary(
        test_video['title'],
        test_video['description'],
        test_video['channel']
    )
    
    print("\nGenerated Summary:")
    print(summary)

if __name__ == "__main__":
    main() 