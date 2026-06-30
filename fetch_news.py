import feedparser
import json
import os
import google.generativeai as genai

# Authenticate with your free Gemini key
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

def fetch_and_summarize():
    # Economic Times Pharma Top Stories
    rss_url = "https://pharma.economictimes.indiatimes.com/rss/topstories"
    feed = feedparser.parse(rss_url)
    
    news_list = []
    
    # Process the 10 most recent articles to keep generation fast
    for entry in feed.entries[:10]:
        title = entry.title
        link = entry.link
        
        prompt = f"Summarize this news article in 50-60 words for a mobile screen. Keep it punchy and factual. Title: {title}. Snippet: {entry.get('summary', '')}"
        
        try:
            response = model.generate_content(prompt)
            summary = response.text.strip()
        except Exception:
            summary = "Summary could not be generated at this time."
            
        news_list.append({
            "title": title,
            "summary": summary,
            "link": link,
            "source": "ET Pharma"
        })
        
    # Save for the frontend to read
    with open('news.json', 'w') as f:
        json.dump(news_list, f, indent=4)

if __name__ == "__main__":
    fetch_and_summarize()
