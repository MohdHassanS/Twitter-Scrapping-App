import streamlit as st
from streamlit_option_menu import option_menu
import snscrape.modules.twitter as sntwitter
import pandas as pd
import pymongo
import datetime
import time
import json

with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",
        options=["Home", "How it works", "Project", "About Me"],
        icons=["house", "binoculars", "app-indicator", "person-video3"],
        menu_icon="cast",
        default_index=0,
    )

if selected == "Home":

    st.header("Welcome to my Tweet scrapping App ")
    st.subheader("Intro")
    st.write(
        """
        Today, data is scattered everywhere in the world."
        - Especially in social media, there may be a big quantity of data on Facebook, Instagram, Youtube, **Twitter**, etc.
        - This consists of pictures and films on Youtube and Instagram as compared to Facebook and Twitter.
        - To get the real facts on Twitter, we can scrape the data from Twitter.
        - We can Scrape the data like (date, id, url, tweet content, user,reply count, retweet count,language, source, like count, etc..) from twitter.
        """
            )

    st.subheader("Why?")
    st.write("Scraping Twitter can yield many insights into sentiments, opinions and social media trends.")
    st.write("Analysing tweets, shares, likes, URLs and interests is a powerful way to derive insight into public conversations.")

    st.subheader("5 Ways To Use Twitter Data For Businesses")
    with st.expander("1.Understanding Customers"):
        st.write("Twitter is a deep resource of customer insights. By surveying brand or product mentions, businesses can analyse the conversations surrounding their brands or products. Twitter today is widely used for customer service, and many people tag brands when they need assistance. This data can be mined and analysed for common issues or complaints. This also extends to positive customer experiences or discussions. ")
    with st.expander("2.Influencer Marketing"):
        st.write("Scraping Twitter data can help locate potential influencers. For example, industry-specific keywords and tags can reveal top posters. This provides opportunities to reach out to influencers via Twitter or another platform. Moreover, Twitter data helps you find what hashtags influencers are using so you can copy these to get noticed in similar hashtag streams. ")
    with st.expander("3.Brand and Reputation Monitoring"):
        st.write("Brand reputations are particularly important on Twitter. Negative stories have been proven to travel faster on Twitter than positive ones. Monitoring brand mentions and reputational comments allows businesses to quickly stub out any false negative stories, or respond to true negative stories promptly to mitigate reputational damage. Brand and product monitoring also help businesses improve services and products and provide on-hand advice to common issues. ")
    with st.expander("4.Sentiment Analysis"):
        st.write("Sentiment analysis targets the semantic meaning of tweets and content, i.e. their emotions. For example, if customers report positive sentiments around a brand or products using words such as ‘super, excellent, happy, content,’ etc, this is a positive sign. Conversely, if customers report negative sentiments such as ‘unhappy, annoyed, frustrated,’ etc, then this is a sign that the brand should intervene. Sentiments can help design customer service and even shape product and service improvements.")
    with st.expander("5.Competitor Monitoring"):
        st.write("All of these techniques can be applied to competitors. It’s possible to analyse sentiments surrounding competitor products or services, or discover what competitors are doing well (or badly), so you can respond strategically. Monitoring competitors’ campaigns and Twitter strategies also reveal insights into how your brand can match or beat their winning tactics. ")


if selected == "How it works":

    st.header("Working Process")
    st.subheader("Stage 1 :")
    st.write(
        """
        - Enter all your inputs correctly.
        - Now press search button.
        """
            )

    st.subheader("Stage 2 :")
    st.write(
        """
        - It will collect the Data based on your Inputs.
        - And displays it in a Table format.
        """
            )

    st.subheader("Stage 3 :")
    st.write(
        """
        - You can upload your data into MongoDB.
        - You can download your data in both CSV and JSON format.
        """
            )

if selected == "Project":

    st.header("Tweet scrapping App ")

    my_bar = st.progress(0)
    for percent_complete in range(100):
        time.sleep(0.1)
        my_bar.progress(percent_complete + 1)

    with st.form("my form"):
        keyword = st.text_input("Enter your Keyword or Hashtag to be searched : ", placeholder="#Data_Scientist or #viratkohli")
        starting_date = st.date_input("Starting Date                          : ", value=datetime.date(2022, 1, 1), min_value=datetime.date(2017, 1, 1))
        ending_date = st.date_input("End Date                                 : ", max_value=datetime.date.today())
        no_of_tweets = st.slider("No of Tweets needed                         : ", 50, 500, step=50)
        submit = st.form_submit_button("Search")

    try:

        t = f"{keyword} since:{starting_date} until:{ending_date}"
        tweets_list1 = []
        for i, tweet in enumerate(sntwitter.TwitterSearchScraper(t).get_items()):
            if i > no_of_tweets:
                break
            tweets_list1.append([tweet.date, tweet.id, tweet.url, tweet.content, tweet.username])
        tweets_df1 = pd.DataFrame(tweets_list1, columns=['Datetime', 'Tweet Id', 'Tweet url', 'Text', 'Username'])

        try:
            st.dataframe(tweets_df1, width=900)
        except:
            st.error('There is no data available for your input', icon="🚨")

        st.download_button("Download as CSV", tweets_df1.to_csv(), file_name=f'{keyword}.csv', mime='text/csv')

        try:
            def convert_df(tweets_df1):
                return tweets_df1.to_csv(index=False).encode('utf-8')
            csv = convert_df(tweets_df1)
            st.download_button("Download JSON File", csv, f'{keyword}.json', key='download-json')

        except:
            st.error('json not working', icon="🚨")


        g = tweets_df1.to_dict("r")

        if st.button("Upload into MongoDB"):
            client = pymongo.MongoClient("mongodb://localhost:27017/")
            my_db = client["scrapped_database"]
            my_col = my_db["twitter"]
            my_col.insert_many(g)
            st.success("Uploaded successfully")
            with st.expander("To view MangoDB file"):
                st.write(g)

    except:
        st.error('Enter the Data and Search again ', icon="🚨")

if selected == "About Me":
    st.header("Hi, I am Mohammed Hassan :wave:")
    st.subheader("A Newbie Data Scientist From Mechanical Background")
    st.write("I am passionate about learning python to be more efficient and effective in **AI and ML Projects**")
    st.write("Check out my other projects in [GitHub](https://github.com/MohdHassanS/Assignment-1.git)")



