# ===========================
# ===== Import Packages =====
# ===========================
import pandas as pd
from tqdm import tqdm

import snscrape.modules.twitter as sntwitter

import re, string
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation

import pyLDAvis
import pyLDAvis.sklearn

from wordcloud import WordCloud
import matplotlib.pyplot as plt

# ======================================================================================
# ====================================== Scraping ======================================
# ======================================================================================
print('======================================================================================')
print('====================================== Scraping ======================================')
print('======================================================================================')
print('\n')

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
    tweets_df.to_csv('./output/temp/hashtag_{}.csv'.format(hashtags[user]), index=False)

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
    user_tweets_df.to_csv('./output/temp/userProfile_{}.csv'.format(usernames[user]), index=False)

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
    mentions_tweets_df.to_csv('./output/temp/userMention_{}.csv'.format(keywords[user]), index=False)

print('\n' + '========================= SCRAPE USER MENTION DONE =========================' + '\n')

# ___Concat Dataframe___
df_hashtag_ganjar = pd.read_csv(r"./output/temp/hashtag_ganjarpranowofor2024.csv")
df_hashtag_prabowo = pd.read_csv(r"./output/temp/hashtag_prabowo.csv")
df_hashtag_anies = pd.read_csv(r"./output/temp/hashtag_AniesPresiden2024.csv")
df_hashtag_ahy = pd.read_csv(r"./output/temp/hashtag_AHY.csv")
df_hashtag_ridwan = pd.read_csv(r"./output/temp/hashtag_RidwanKamil.csv")

df_mention_ganjar = pd.read_csv(r"./output/temp/userMention_@ganjarpranowo.csv")
df_mention_prabowo = pd.read_csv(r"./output/temp/userMention_@prabowo.csv")
df_mention_anies = pd.read_csv(r"./output/temp/userMention_@aniesbaswedan.csv")
df_mention_ahy = pd.read_csv(r"./output/temp/userMention_@AgusYudhoyono.csv")
df_mention_ridwan = pd.read_csv(r"./output/temp/userMention_@ridwankamil.csv")

df_userprofile_ganjar = pd.read_csv(r"./output/temp/userProfile_ganjarpranowo.csv")
df_userprofile_prabowo = pd.read_csv(r"./output/temp/userProfile_prabowo.csv")
df_userprofile_anies = pd.read_csv(r"./output/temp/userProfile_aniesbaswedan.csv")
df_userprofile_ahy = pd.read_csv(r"./output/temp/userProfile_AgusYudhoyono.csv")
df_userprofile_ridwan = pd.read_csv(r"./output/temp/userProfile_ridwankamil.csv")

df_ganjar = pd.concat([df_hashtag_ganjar, df_mention_ganjar], ignore_index=True)
df_prabowo = pd.concat([df_hashtag_prabowo, df_mention_prabowo], ignore_index=True)
df_anies = pd.concat([df_hashtag_anies, df_mention_anies], ignore_index=True)
df_ahy = pd.concat([df_hashtag_ahy, df_mention_ahy], ignore_index=True)
df_ridwan = pd.concat([df_hashtag_ridwan, df_mention_ridwan], ignore_index=True)

df_names = [df_ganjar, df_prabowo, df_anies, df_ahy, df_ridwan]
df_profil_names = [df_userprofile_ganjar, df_userprofile_prabowo, df_userprofile_anies, df_userprofile_ahy, df_userprofile_ridwan]
df_string = ['ganjar', 'prabowo', 'anies', 'ahy', 'ridwan']

for df in range(len(df_names)):
    df_names[df].to_csv('./output/data/df_{}.csv'.format(df_string[df]))

print('\n' + '========================= SCRAPING DONE =========================' + '\n')

# ================================================================================================
# ====================================== Sentiment Analysis ======================================
# ================================================================================================
print('================================================================================================')
print('====================================== Sentiment Analysis ======================================')
print('================================================================================================')
print('\n')

# ========================
# ===== Import Model =====
# ========================
pretrained= "mdhugol/indonesia-bert-sentiment-classification"

model = AutoModelForSequenceClassification.from_pretrained(pretrained)
tokenizer = AutoTokenizer.from_pretrained(pretrained)

# ============================
# ===== Model Definition =====
# ============================
sentiment_analysis = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

label_index = {'LABEL_0': 'positive', 'LABEL_1': 'neutral', 'LABEL_2': 'negative'}

# ======================
# ===== Prediction =====
# ======================
for df in tqdm(range(len(df_names))):
    print('\n' + 'Processing {}....'.format(df_string[df]))
    pos_list = []
    neu_list = []
    neg_list = []

    for index, row in tqdm(df_names[df].iterrows()):
        result = sentiment_analysis(row['clean_text'])
        status = label_index[result[0]['label']]

        if status == 'positive':
            pos_list.append(row['clean_text'])
        elif status == 'neutral':
            neu_list.append(row['clean_text'])
        else:
            neg_list.append(row['clean_text'])

    pos_df = pd.DataFrame(pos_list)
    neu_df = pd.DataFrame(neu_list)
    neg_df = pd.DataFrame(neg_list)

    pos_df.to_csv('./output/sentiment/pos_{}.csv'.format(df_string[df]))
    neu_df.to_csv('./output/sentiment/neu_{}.csv'.format(df_string[df]))
    neg_df.to_csv('./output/sentiment/neg_{}.csv'.format(df_string[df]))

print('\n' + '========================= SENTIMENT ANALYSIS DONE =========================' + '\n')

# =======================================================================================
# ====================================== Wordcloud ======================================
# =======================================================================================
print('=======================================================================================')
print('====================================== Wordcloud ======================================')
print('=======================================================================================')
print('\n')

# =====================
# ===== Load Data =====
# =====================
df_pos_ganjar = pd.read_csv(r"./output/sentiment/pos_ganjar.csv")
df_neu_ganjar = pd.read_csv(r"./output/sentiment/neu_ganjar.csv")
df_neg_ganjar = pd.read_csv(r"./output/sentiment/neg_ganjar.csv")

df_pos_prabowo = pd.read_csv(r"./output/sentiment/pos_prabowo.csv")
df_neu_prabowo = pd.read_csv(r"./output/sentiment/neu_prabowo.csv")
df_neg_prabowo = pd.read_csv(r"./output/sentiment/neg_prabowo.csv")

df_pos_anies = pd.read_csv(r"./output/sentiment/pos_anies.csv")
df_neu_anies = pd.read_csv(r"./output/sentiment/neu_anies.csv")
df_neg_anies = pd.read_csv(r"./output/sentiment/neg_anies.csv")

df_pos_ahy = pd.read_csv(r"./output/sentiment/pos_ahy.csv")
df_neu_ahy = pd.read_csv(r"./output/sentiment/neu_ahy.csv")
df_neg_ahy = pd.read_csv(r"./output/sentiment/neg_ahy.csv")

df_pos_ridwan = pd.read_csv(r"./output/sentiment/pos_ridwan.csv")
df_neu_ridwan = pd.read_csv(r"./output/sentiment/neu_ridwan.csv")
df_neg_ridwan = pd.read_csv(r"./output/sentiment/neg_ridwan.csv")

df_sens = [[df_pos_ganjar, df_neu_ganjar, df_neg_ganjar], [df_pos_prabowo, df_neu_prabowo, df_neg_prabowo],
[df_pos_anies, df_neu_anies, df_neg_anies], [df_pos_ahy, df_neu_ahy, df_neg_ahy],
[df_pos_ridwan, df_neu_ridwan, df_neg_ridwan]]

# =============================
# ===== Wordcloud Mention =====
# =============================
labels = ['pos', 'neu', 'neg']
print('Processing mention wordcloud images...')

# ___Join list as 1 string, and save wordcloud image___
for df_list in tqdm(range(len(df_sens))):
    print('Processing {}'.format(df_string[df_list]))
    for branch in range(len(df_sens[df_list])):
        text_content = list(df_sens[df_list][branch]['0'])

        text_string = ''
        for elem in text_content:
            text_string = ' '.join([text_string, str(elem)])
        
        # Colour
        if branch == 0:
            wordcloud = WordCloud(background_color='white', width=2000, height=1000, colormap='summer').generate(text_string)
        elif branch == 1:
            wordcloud = WordCloud(background_color='white', width=2000, height=1000).generate(text_string)
        else:
            wordcloud = WordCloud(background_color='white', width=2000, height=1000, colormap='gist_heat').generate(text_string)

        # plot wordcloud
        plt.figure(figsize=(25,15))
        image = plt.imshow(wordcloud)

        # Hapus nilai axis
        plt.axis('off')
        plt.tight_layout(pad=0)
        plt.savefig('./output/wordcloud/{}/wordcloud_mention_{}_{}.jpg'.format(df_string[df_list], df_string[df_list], labels[branch]))

# =============================
# ===== Wordcloud Profile =====
# =============================
print('Processing profile wordcloud images...')
# ___Join list as 1 string, and save wordcloud image___
for df in tqdm(range(len(df_profil_names))):
    text_content = list(df_profil_names[df]['clean_text_stem'])

    text_string = ''
    for elem in text_content:
        text_string = ' '.join([text_string, str(elem)])

    wordcloud = WordCloud(background_color='white', width=2000, height=1000, colormap='summer').generate(text_string)

    # plot wordcloud
    plt.figure(figsize=(25,15))
    image = plt.imshow(wordcloud)

    # Hapus nilai axis
    plt.axis('off')
    plt.tight_layout(pad=0)
    plt.savefig('./output/wordcloud/wordcloud_profile_{}.jpg'.format(df_string[df]))

print('\n' + '========================= WORDCLOUD DONE =========================' + '\n')

# =========================================================================================
# ====================================== Topic Model ======================================
# =========================================================================================
print('=========================================================================================')
print('====================================== Topic Model ======================================')
print('=========================================================================================')
print('\n')

tfidf_vectorizer = TfidfVectorizer()

for df in tqdm(range(len(df_names))):
    # ___apply TF-IDF___
    dtm_tfidf = tfidf_vectorizer.fit_transform(list(df_names[df]['clean_text_stem']))

    # ___apply LDA___
    lda_tfidf = LatentDirichletAllocation(n_components=10)
    lda_tfidf.fit(dtm_tfidf)

    # ___export HTML___
    data = pyLDAvis.sklearn.prepare(lda_tfidf, dtm_tfidf, tfidf_vectorizer)
    pyLDAvis.save_html(data, './output/topic/lda_{}.html'.format(df_string[df]))

print('======================================================================================')
print('====================================== ALL DONE ======================================')
print('======================================================================================')