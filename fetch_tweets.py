import time
import tweepy
import configparser
import pandas as pd
import nltk

# Download the VADER lexicon
nltk.download('vader_lexicon')

# Step 1: Load API Credentials
config = configparser.ConfigParser()
config.read('config.ini')

api_key = config['twitter']['api_key']
api_key_secret = config['twitter']['api_key_secret']
bearer_token = config['twitter']['bearer_token']

# Step 2: Initialize Tweepy Client with rate limit handling
client = tweepy.Client(bearer_token=bearer_token, wait_on_rate_limit=True)

# Step 3: Define the Hashtag to Search
hashtag = "#Python"
query = f"{hashtag} -is:retweet lang:en"  # Exclude retweets, English only
max_results = 30  # Number of tweets to fetch

def fetch_tweets():
    try:
        # Fetch Tweets
        tweets = client.search_recent_tweets(query=query, tweet_fields=['author_id', 'created_at'], max_results=max_results)
        
        # Check if there are tweets
        if tweets.data:
            columns = ['Tweet ID', 'Author ID', 'Created At', 'Tweet Text']
            data = []
            for tweet in tweets.data:
                data.append([tweet.id, tweet.author_id, tweet.created_at, tweet.text])

            # Create a DataFrame
            df = pd.DataFrame(data, columns=columns)

            # Save to CSV
            df.to_csv('tweets.csv', index=False)
            return df
        else:
            return None

    except tweepy.errors.TooManyRequests as e:
        print(f"Rate limit exceeded. Sleeping for {e.response.headers['x-rate-limit-reset']} seconds.")
        reset_time = int(e.response.headers['x-rate-limit-reset'])
        sleep_duration = reset_time - time.time() + 5  # 5 seconds buffer
        time.sleep(sleep_duration)  # Sleep until the rate limit is reset
        return fetch_tweets()  # Retry after the rate limit reset

# Call the function to fetch tweets
df = fetch_tweets()
if df is not None:
    print("Fetched tweets successfully.")
else:
    print("No tweets found.")
