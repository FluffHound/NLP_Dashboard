# ===========================
# ===== Import Packages =====
# ===========================
import pandas as pd
from tqdm import tqdm

import snscrape.modules.twitter as sntwitter

import re, string
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

# ===============================
# ===== Preprocess Function =====
# ===============================
# ___Remove Rubbish___
def clean_text(text): # credit to Fathur
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
dictionary = StopWordRemoverFactory().get_stop_words()
dictionary += ['yg', 'vs', 'cebong', 'utk', 'sy', 'jg', 'sbg', 'kpd', 'ttg', 'moga', 'lu', 'loe', 'doang', 'ak',
                'si', 'gak', 'dgn', 'dlm']

def removeStop(text):
    words = text.split(' ')
    stopped_words = [word for word in words if not word in dictionary]
    return ' '.join(stopped_words)

# ___jumlah scrap___
num_scrap = 1000
print('Scraping', str(num_scrap), 'tweet data')

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
        if i > num_scrap:
            break
        tweets_list.append([tweet.id, tweet.date, tweet.user.username, tweet.content])

    tweets_df = pd.DataFrame(tweets_list, columns=['id', 'dateTime', 'userName', 'content'])

    # ___Cleaning, Stemming, Remove Stopwords, Remove Blank Text, Tokenize___
    tweets_df['clean_text'] = tweets_df['content'].apply(lambda x: clean_text(x))
    tweets_df['clean_text'] = tweets_df['clean_text'].apply(lambda x: removeStop(x))
    tweets_df['clean_text_stem'] = tweets_df['clean_text'].apply(lambda x: stemmer.stem(x))
    tweets_df.replace("", float("NaN"), inplace=True) # Menghapus baris kosong setelah dihapus stopword
    tweets_df = tweets_df.dropna()
    tweets_df.reset_index(drop=True)

    # ___Export Data___
    tweets_df.to_csv('./data_clean/hashtag_{}.csv'.format(hashtags[user]), index=False)

print('\n' + '========================= SCRAPE HASHTAG DONE =========================' + '\n')

# =======================================
# ===== Scrap User Profile's Tweets =====
# =======================================
for user in range(len(usernames)):
    print('\n' + 'Scraping @' + usernames[user] + '...')
    # ___User Profile scraper___
    user_profile_list = []

    for i, tweet in enumerate(tqdm(sntwitter.TwitterUserScraper(usernames[user]).get_items())):
        if i > num_scrap:
            break
        user_profile_list.append([tweet.id, tweet.date, tweet.likeCount, tweet.content])

    user_tweets_df = pd.DataFrame(user_profile_list, columns=['id', 'dateTime', 'likes', 'content'])

# ___Cleaning, Stemming, Remove Stopwords, Remove Blank Text, Tokenize___
    user_tweets_df['clean_text'] = user_tweets_df['content'].apply(lambda x: clean_text(x))
    user_tweets_df['clean_text'] = user_tweets_df['clean_text'].apply(lambda x: removeStop(x))
    user_tweets_df['clean_text_stem'] = user_tweets_df['clean_text'].apply(lambda x: stemmer.stem(x))
    user_tweets_df.replace("", float("NaN"), inplace=True) # Menghapus baris kosong setelah dihapus stopword
    user_tweets_df = user_tweets_df.dropna()
    user_tweets_df.reset_index(drop=True)

    # ___Export Data___
    user_tweets_df.to_csv('./data_clean/userProfile_{}.csv'.format(usernames[user]), index=False)

print('\n' + '========================= SCRAPE USER PROFILE DONE =========================' + '\n')

# =======================================
# ===== Scrap Mentions Tweets =====
# =======================================
for user in range(len(keywords)):
    print('\n' + 'Scraping mentions of ' + keywords[user] + '...')
    # ___User Profile scraper___
    user_mention_list = []

    for i, tweet in enumerate(tqdm(sntwitter.TwitterSearchScraper(keywords[user]).get_items())):
        if i > num_scrap:
            break
        user_mention_list.append([tweet.id, tweet.date, tweet.user.username, tweet.content])

    mentions_tweets_df = pd.DataFrame(user_mention_list, columns=['id', 'dateTime', 'userName', 'content'])

    # ___Cleaning, Stemming, Remove Stopwords, Remove Blank Text, Tokenize___
    mentions_tweets_df['clean_text'] = mentions_tweets_df['content'].apply(lambda x: clean_text(x))
    mentions_tweets_df['clean_text'] = mentions_tweets_df['clean_text'].apply(lambda x: removeStop(x))
    mentions_tweets_df['clean_text_stem'] = mentions_tweets_df['clean_text'].apply(lambda x: stemmer.stem(x))
    mentions_tweets_df.replace("", float("NaN"), inplace=True) # Menghapus baris kosong setelah dihapus stopword
    mentions_tweets_df = mentions_tweets_df.dropna()
    mentions_tweets_df.reset_index(drop=True)

    # ___Export Data___
    mentions_tweets_df.to_csv('./data_clean/userMention_{}.csv'.format(keywords[user]), index=False)

print('\n' + '========================= SCRAPE USER MENTION DONE =========================' + '\n')

print('ALL DONE!')