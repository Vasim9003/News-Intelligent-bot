import requests
from bs4 import BeautifulSoup

def get_tech_news():
    # TechCrunch RSS Feed URL
    url = "news.google.com/rss"
    
    response = requests.get(url)
    
    soup = BeautifulSoup(response.content, features="xml")
    
    articles = soup.find_all('item')
    
    print(f"Total articles found: {len(articles)}")
    print("-" * 30)

    for article in articles:
        title = article.title.text
        link = article.link.text
        description = article.description.text if article.description else "No description"

        if "layoff" in title.lower() or "job cut" in title.lower():
            print(f"📍 NEWS FOUND: {title}")
            print(f"Link: {link}")
            print(f"Summary: {description[:100]}...")
            print("-" * 30)

if __name__ == "__main__":
    get_tech_news()
