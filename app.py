import streamlit as st
import pandas as pd
import tweepy
import configparser
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Step 1: Load API Credentials and Fetch Tweets
def fetch_tweets():
    config = configparser.ConfigParser()
    config.read('config.ini')

    api_key = config['twitter']['api_key']
    api_key_secret = config['twitter']['api_key_secret']
    bearer_token = config['twitter']['bearer_token']

    # Initialize Tweepy Client
    client = tweepy.Client(bearer_token=bearer_token)

    hashtag = "#Python"  # Example hashtag
    query = f"{hashtag} -is:retweet lang:en"  # Exclude retweets, English only
    max_results = 100  # Number of tweets to fetch

    # Fetch Tweets
    tweets = client.search_recent_tweets(query=query, tweet_fields=['author_id', 'created_at'], max_results=max_results)

    columns = ['Tweet ID', 'Author ID', 'Created At', 'Tweet Text']
    data = []

    if tweets.data:
        for tweet in tweets.data:
            data.append([tweet.id, tweet.author_id, tweet.created_at, tweet.text])

        df = pd.DataFrame(data, columns=columns)
        df.to_csv('tweets.csv', index=False)
        return df
    else:
        return None


# Step 2: Sentiment Analysis using VADER
def sentiment_analysis(df):
    analyzer = SentimentIntensityAnalyzer()
    df['Sentiment'] = df['Tweet Text'].apply(lambda x: analyzer.polarity_scores(x)['compound'])
    df['Sentiment Label'] = df['Sentiment'].apply(lambda x: 'Positive' if x > 0.1 else ('Negative' if x < -0.1 else 'Neutral'))
    return df


# Step 3: Extract Hashtags
def extract_hashtags(df):
    hashtags = []
    for tweet in df['Tweet Text']:
        hashtags.extend(re.findall(r'#\w+', tweet))
    return hashtags


# Step 4: Create a Word Cloud
def create_word_cloud(df):
    text = ' '.join(df['Tweet Text'])
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    return wordcloud


# Streamlit UI
st.title("Twitter Hashtag Analysis")

st.sidebar.title("Options")
option = st.sidebar.selectbox("Choose an option", ["Fetch Tweets", "View Analysis"])

if option == "Fetch Tweets":
    st.write("Fetching tweets with the hashtag #Python...")
    df = fetch_tweets()
    if df is not None:
        st.write(f"Fetched {len(df)} tweets.")
    else:
        st.write("No tweets found for the given hashtag.")
        
if option == "View Analysis":
    try:
        df = pd.read_csv('tweets.csv')
        # Sentiment analysis
        df = sentiment_analysis(df)
        
        # Show sentiment distribution
        sentiment_counts = df['Sentiment Label'].value_counts()
        st.subheader("Sentiment Distribution")
        st.bar_chart(sentiment_counts)

        # Top Hashtags
        st.subheader("Top Hashtags")
        hashtags = extract_hashtags(df)
        hashtag_counts = pd.Series(hashtags).value_counts().head(10)
        st.write(hashtag_counts)

        # Display Word Cloud
        # Display Word Cloud
        st.subheader("Word Cloud")
        wordcloud = create_word_cloud(df)

        # Create a figure
        fig, ax = plt.subplots(figsize=(10, 5))

        # Display the wordcloud
        ax.imshow(wordcloud, interpolation="bilinear")
        ax.axis("off")

        # Display the figure in Streamlit
        st.pyplot(fig)


    except Exception as e:
        st.write(f"Error: {e}")
