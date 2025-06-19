import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize Gemini model
model = genai.GenerativeModel('gemini-pro')

def get_ai_response(user_input):
    """
    Get AI response using Gemini model
    """
    prompt = f"""
    Based on the user's query: "{user_input}"
    
    Please provide:
    1. A brief explanation of the topic
    2. 3-5 recommended topics or keywords that would be good to search on YouTube
    3. What specific type of videos would be most helpful for this topic
    
    Format your response in a clear, structured way with sections.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error processing with Gemini: {e}"

def main():
    print("🤖 AI Learning Assistant")
    print("This assistant will help you learn about any topic and suggest what to look for on YouTube")
    print("Type 'quit' to exit")
    
    while True:
        user_input = input("\n🔍 What would you like to learn about? ")
        
        if user_input.lower() == 'quit':
            print("\nThank you for using the AI Learning Assistant! Goodbye! 👋")
            break
            
        print("\nThinking... 🤔\n")
        
        # Get AI response
        response = get_ai_response(user_input)
        print(response)
        print("\n" + "="*50)

if __name__ == "__main__":
    main() 