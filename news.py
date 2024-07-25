import requests
import sensetive_info

API_KEY =  sensetive_info.NEWS_API_KEY # Replace with your actual News API key
NEWS_API_URL = sensetive_info.NEWS_API_KEY_URL # Replace with the URL for the News API
def get_daily_news():
    params = {
        'country': 'us',  # You can change this to your preferred country
        'apiKey': API_KEY
    }
    response = requests.get(NEWS_API_URL, params=params)
    if response.status_code == 200:
        news_data = response.json()
        print("Today's Top News Headlines:")
        for article in news_data['articles']:
            print(f"- {article['title']}")
            print(f"  URL: {article['url']}\n")
    else:
        print("Failed to retrieve news")

if __name__ == "__main__":
    get_daily_news()