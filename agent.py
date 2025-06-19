import os
from dotenv import load_dotenv
from youtube_search import YouTubeSearchAgent
import json
import re

# Load environment variables
load_dotenv()

class AIAgent:
    def __init__(self):
        self.youtube_agent = YouTubeSearchAgent()
        
    def process_query(self, user_input):
        """
        Process user input to extract search parameters and intent
        """
        # Convert common question patterns to search queries
        query = user_input.lower()
        
        # Remove question words and convert to search terms
        query = re.sub(r'^(how|what|where|who|when|why|can you|could you|please|i want|show me|find|search for)\s+', '', query)
        query = re.sub(r'\?+$', '', query)
        
        # Handle different types of queries
        if "tutorial" in query or "how to" in query or "learn" in query:
            return self.handle_tutorial_query(query)
        elif "news" in query or "latest" in query or "recent" in query:
            return self.handle_news_query(query)
        else:
            return self.handle_general_query(query)

    def handle_tutorial_query(self, query):
        """
        Handle queries related to tutorials and learning
        """
        print(f"\nLooking for educational content about: {query}")
        # Add tutorial-specific parameters
        videos = self.youtube_agent.search_videos(
            query + " tutorial",
            max_results=5
        )
        return self.format_results(videos, "Tutorial Results")

    def handle_news_query(self, query):
        """
        Handle queries related to news and recent content
        """
        print(f"\nSearching for latest content about: {query}")
        # Add news-specific parameters
        videos = self.youtube_agent.search_videos(
            query + " news",
            max_results=5
        )
        return self.format_results(videos, "Latest Results")

    def handle_general_query(self, query):
        """
        Handle general search queries
        """
        print(f"\nSearching for: {query}")
        videos = self.youtube_agent.search_videos(query)
        return self.format_results(videos, "Search Results")

    def format_results(self, videos, section_title):
        """
        Format the video results in a user-friendly way
        """
        if not videos:
            return "No videos found for your query."

        output = [f"\n=== {section_title} ===\n"]
        
        for i, video in enumerate(videos, 1):
            # Get additional details for each video
            details = self.youtube_agent.get_video_details(video['video_id'])
            
            output.append(f"{i}. {video['title']}")
            output.append(f"   Channel: {video['channel']}")
            output.append(f"   🔗 {video['url']}")
            
            if details:
                output.append(f"   Views: {int(details['views']):,}")
                output.append(f"   Likes: {details['likes']}")
                output.append(f"   Comments: {details['comments']}")
            
            # Add a brief description (first 100 characters)
            desc = video['description'][:100].replace('\n', ' ').strip()
            output.append(f"   Description: {desc}...")
            output.append("")  # Empty line between videos
            
        return "\n".join(output)

def main():
    print("🤖 AI Video Search Assistant")
    print("I can help you find YouTube videos on any topic!")
    print("Examples of what you can ask:")
    print("- 'How to make pasta?'")
    print("- 'Show me the latest news about AI'")
    print("- 'Find guitar tutorials for beginners'")
    print("\nType 'quit' to exit")
    
    agent = AIAgent()
    
    while True:
        user_input = input("\n💭 What would you like to learn about? ")
        
        if user_input.lower() == 'quit':
            print("\nThank you for using the AI Video Search Assistant! Goodbye! 👋")
            break
        
        if not user_input.strip():
            print("Please enter a search query!")
            continue
            
        print("\nThinking... 🤔")
        
        try:
            result = agent.process_query(user_input)
            print(result)
            print("\n" + "="*50)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            print("Please try a different search query.")

if __name__ == "__main__":
    main() 