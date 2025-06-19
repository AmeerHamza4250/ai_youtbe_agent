import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Load environment variables
load_dotenv()

class YouTubeSearchAgent:
    def __init__(self):
        self.api_key = os.getenv('YOUTUBE_API_KEY')
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)

    def search_videos(self, query, max_results=5):
        """
        Search for YouTube videos based on a query
        """
        try:
            # Call the search.list method to retrieve results
            search_response = self.youtube.search().list(
                q=query,
                part='snippet',
                maxResults=max_results,
                type='video',
                order='relevance'
            ).execute()

            videos = []
            for item in search_response.get('items', []):
                video_data = {
                    'title': item['snippet']['title'],
                    'video_id': item['id']['videoId'],
                    'channel': item['snippet']['channelTitle'],
                    'description': item['snippet']['description'],
                    'url': f"https://www.youtube.com/watch?v={item['id']['videoId']}"
                }
                videos.append(video_data)

            return videos

        except HttpError as e:
            print(f"An HTTP error {e.resp.status} occurred: {e.content}")
            return []
        except Exception as e:
            print(f"An error occurred: {e}")
            return []

    def get_video_details(self, video_id):
        """
        Get detailed information about a specific video
        """
        try:
            video_response = self.youtube.videos().list(
                part='snippet,statistics',
                id=video_id
            ).execute()

            if video_response['items']:
                video = video_response['items'][0]
                return {
                    'title': video['snippet']['title'],
                    'views': video['statistics']['viewCount'],
                    'likes': video['statistics'].get('likeCount', 'N/A'),
                    'comments': video['statistics'].get('commentCount', 'N/A')
                }
            return None

        except HttpError as e:
            print(f"An HTTP error {e.resp.status} occurred: {e.content}")
            return None

def main():
    print("🎥 YouTube Search Agent")
    print("Type 'quit' to exit")
    
    agent = YouTubeSearchAgent()
    
    while True:
        query = input("\nEnter your search query: ")
        
        if query.lower() == 'quit':
            print("\nThank you for using YouTube Search Agent! Goodbye! 👋")
            break
        
        print("\nSearching for videos... 🔍")
        videos = agent.search_videos(query)
        
        if videos:
            print("\nFound these videos:")
            for i, video in enumerate(videos, 1):
                print(f"\n{i}. {video['title']}")
                print(f"   Channel: {video['channel']}")
                print(f"   🔗 {video['url']}")
                print(f"   Description: {video['description'][:100]}...")
                
                # Get and display video details
                details = agent.get_video_details(video['video_id'])
                if details:
                    print(f"   Views: {details['views']:,}")
                    print(f"   Likes: {details['likes']}")
                    print(f"   Comments: {details['comments']}")
        else:
            print("No videos found for your query.")
        
        print("\n" + "="*50)

if __name__ == "__main__":
    main() 