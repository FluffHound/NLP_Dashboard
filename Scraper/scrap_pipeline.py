# ===========================
# ===== Import Packages =====
# ===========================
import pandas as pd
import numpy as np
from tqdm import tqdm

import snscrape.modules.twitter as sntwitter

import re, string
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from nltk.tokenize import word_tokenize

from wordcloud import WordCloud
import matplotlib.pyplot as plt

# ===============================
# ===== Preprocess Function =====
# ===============================
# ___Remove Rubbish___
def clean_text(text):
    text = str(text)
    text = text.lower()
    text = re.sub("@[A-Za-z0-9_]+", "", text)  # Menghapus @<name> [mention twitter]
    text = re.sub("#\w+", "", text) # Menghapus hashtag #
    text = re.sub("\[.*?\]", "", text)  # Menghapus [string]
    text = re.sub("https?://\S+|www\.\S+", "", text)    # Menghapus link
    text = re.sub("<.*?>+", "", text)   # Menghapus <string>
    text = re.sub("[%s]" % re.escape(string.punctuation), "", text) # Menghapus tanda baca
    text = re.sub("\w*\d\w*", "", text) # Menghapus kata + angka ex: t0g3l
    text = re.sub("\d+", "", text)  # Menghapus kata diawali huruf ex: 45merdeka
    text = re.sub("amp", " ", text) # Menghapus &amp; pada kata
    text = re.sub("\s+", " ", text).strip() # Menghapus whitespace di antara kata
    text = text.replace("\n", " ")  # Menghapus tag newline
    text = " ".join(text.split())
    return text

# ___Stemming___
factory = StemmerFactory()
stemmer = factory.create_stemmer()

# ___Stopword___
factory_stop = StopWordRemoverFactory()
stopword = factory_stop.create_stop_word_remover()

# ___Tokenizing___
def word_tokenize_wrapper(text):
  return word_tokenize(text)

# ===========================
# ===== Things to Query =====
# ===========================
hashtags = ['ganjarpranowofor2024', 'prabowo', 'AniesPresiden2024', 'AHY', 'RidwanKamil']
usernames = ['ganjarpranowo', 'prabowo', 'aniesbaswedan', 'AgusYudhoyono', 'ridwankamil']
keywords = ['@ganjarpranowo', '@prabowo', '@aniesbaswedan', '@AgusYudhoyono', '@ridwankamil']

# ==========================
# ===== Scrap Hashtags =====
# ==========================
for user in range(len(hashtags)):
    print('\n' + 'Scraping #' + hashtags[user] + '...')
    # ___Hashtag scraper___
    tweets_list = []

    for i, tweet in enumerate(tqdm(sntwitter.TwitterHashtagScraper(hashtags[user]).get_items())):
        if i > 50:
            break
        tweets_list.append([tweet.id, tweet.date, tweet.user.username, tweet.content])

    tweets_df = pd.DataFrame(tweets_list, columns=['ID', 'Datetime', 'Username', 'Content'])

    # ___Cleaning, Stemming, Remove Stopwords, Remove Blank Text, Tokenize___
    tweets_df['clean_text'] = tweets_df['Content'].apply(lambda x: clean_text(x))
    tweets_df['clean_text'] = tweets_df['clean_text'].apply(lambda x: stemmer.stem(x))
    tweets_df['clean_text'] = tweets_df['clean_text'].apply(lambda x: stopword.remove(x))
    tweets_df.replace("", float("NaN"), inplace=True)
    tweets_df = tweets_df.dropna()
    tweets_df['text_token'] = tweets_df['clean_text'].apply(word_tokenize_wrapper)

    # ___Export Data___
    tweets_df.to_csv('./data_clean/hashtag_{}.csv'.format(hashtags[user]), sep=';', index=False)

print('\n' + '========================= SCRAPE HASHTAG DONE =========================' + '\n')

# =======================================
# ===== Scrap User Profile's Tweets =====
# =======================================
for user in range(len(usernames)):
    print('\n' + 'Scraping @' + usernames[user] + '...')
    # ___User Profile scraper___
    user_profile_list = []

    for i, tweet in enumerate(tqdm(sntwitter.TwitterUserScraper(usernames[user]).get_items())):
        if i > 50:
            break
        user_profile_list.append([tweet.id, tweet.date, tweet.likeCount, tweet.content])

    user_tweets_df = pd.DataFrame(user_profile_list, columns=['ID', 'Datetime', 'Likes', 'Content'])

# ___Cleaning, Stemming, Remove Stopwords, Remove Blank Text, Tokenize___
    user_tweets_df['clean_text'] = user_tweets_df['Content'].apply(lambda x: clean_text(x))
    user_tweets_df['clean_text'] = user_tweets_df['clean_text'].apply(lambda x: stemmer.stem(x))
    user_tweets_df['clean_text'] = user_tweets_df['clean_text'].apply(lambda x: stopword.remove(x))
    user_tweets_df.replace("", float("NaN"), inplace=True)
    user_tweets_df = user_tweets_df.dropna()
    user_tweets_df['text_token'] = user_tweets_df['clean_text'].apply(word_tokenize_wrapper)

    # ___Export Data___
    user_tweets_df.to_csv('./data_clean/userProfile_{}.csv'.format(usernames[user]), sep=';', index=False)

print('\n' + '========================= SCRAPE USER PROFILE DONE =========================' + '\n')

# =======================================
# ===== Scrap Mentions Tweets =====
# =======================================
for user in range(len(keywords)):
    print('\n' + 'Scraping mentions of @' + keywords[user] + '...')
    # ___User Profile scraper___
    user_mention_list = []

    for i, tweet in enumerate(tqdm(sntwitter.TwitterSearchScraper(keywords[user]).get_items())):
        if i > 50:
            break
        user_mention_list.append([tweet.id, tweet.date, tweet.user.username, tweet.content])

    mentions_tweets_df = pd.DataFrame(user_mention_list, columns=['ID', 'Datetime', 'Username', 'Content'])

    # ___Cleaning, Stemming, Remove Stopwords, Remove Blank Text, Tokenize___
    mentions_tweets_df['clean_text'] = mentions_tweets_df['Content'].apply(lambda x: clean_text(x))
    mentions_tweets_df['clean_text'] = mentions_tweets_df['clean_text'].apply(lambda x: stemmer.stem(x))
    mentions_tweets_df['clean_text'] = mentions_tweets_df['clean_text'].apply(lambda x: stopword.remove(x))
    mentions_tweets_df.replace("", float("NaN"), inplace=True)
    mentions_tweets_df = mentions_tweets_df.dropna()
    mentions_tweets_df['text_token'] = mentions_tweets_df['clean_text'].apply(word_tokenize_wrapper)

    # ___Export Data___
    mentions_tweets_df.to_csv('./data_clean/userMention_{}.csv'.format(keywords[user]), sep=';', index=False)

print('\n' + '========================= SCRAPE USER MENTION DONE =========================' + '\n')

print('ALL DONE!')