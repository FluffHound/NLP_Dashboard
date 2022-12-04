# ===========================
# ===== Import Packages =====
# ===========================
import pandas as pd
import numpy as np
from tqdm import tqdm

# import re, string
# from nltk.tokenize import word_tokenize

from wordcloud import WordCloud
import matplotlib.pyplot as plt

# ===============================
# ===== Import Data Mention =====
# ===============================
df_hashtag_ganjar = pd.read_json(r"..\Scraper\data_clean\hashtag_ganjarpranowofor2024.json")
df_hashtag_prabowo = pd.read_json(r"..\Scraper\data_clean\hashtag_prabowo.json")
df_hashtag_anies = pd.read_json(r"..\Scraper\data_clean\hashtag_AniesPresiden2024.json")
df_hashtag_ahy = pd.read_json(r"..\Scraper\data_clean\hashtag_AHY.json")
df_hashtag_ridwan = pd.read_json(r"..\Scraper\data_clean\hashtag_RidwanKamil.json")

df_mention_ganjar = pd.read_json(r"..\Scraper\data_clean\userMention_@ganjarpranowo.json")
df_mention_prabowo = pd.read_json(r"..\Scraper\data_clean\userMention_@prabowo.json")
df_mention_anies = pd.read_json(r"..\Scraper\data_clean\userMention_@aniesbaswedan.json")
df_mention_ahy = pd.read_json(r"..\Scraper\data_clean\userMention_@AgusYudhoyono.json")
df_mention_ridwan = pd.read_json(r"..\Scraper\data_clean\userMention_@ridwankamil.json")

# ___Concat Dataframe___
df_ganjar = pd.concat([df_hashtag_ganjar, df_mention_ganjar], ignore_index=True)
df_prabowo = pd.concat([df_hashtag_prabowo, df_mention_prabowo], ignore_index=True)
df_anies = pd.concat([df_hashtag_anies, df_mention_anies], ignore_index=True)
df_ahy = pd.concat([df_hashtag_ahy, df_mention_ahy], ignore_index=True)
df_ridwan = pd.concat([df_hashtag_ridwan, df_mention_ridwan], ignore_index=True)

df_names = [df_ganjar, df_prabowo, df_anies, df_ahy, df_ridwan]
df_string = ['ganjar', 'prabowo', 'anies', 'ahy', 'ridwan']

# =====================
# ===== Wordcloud =====
# =====================
print('Processing mention wordcloud images...')
# ___Join list as 1 string, and save wordcloud image___
for df in tqdm(range(len(df_names))):
    text_content = list(df_names[df]['clean_text_stem'])

    text_string = ''
    for elem in text_content:
        text_string = ' '.join([text_string, str(elem)])

    wordcloud = WordCloud(background_color='white').generate(text_string)

    # plot wordcloud
    plt.figure(figsize=(25,15))
    image = plt.imshow(wordcloud)

    # Hapus nilai axis
    plt.axis('off')
    # plt.show()
    # plt.imsave('wordcloud_{}.jpg'.format(df[3:]), arr=image)
    plt.savefig('./output/wordcloud_mention_{}.jpg'.format(df_string[df]))

# ===============================
# ===== Import Data Profile =====
# ===============================
df_userprofile_ganjar = pd.read_json(r"..\Scraper\data_clean\userProfile_ganjarpranowo.json")
df_userprofile_prabowo = pd.read_json(r"..\Scraper\data_clean\userProfile_prabowo.json")
df_userprofile_anies = pd.read_json(r"..\Scraper\data_clean\userProfile_aniesbaswedan.json")
df_userprofile_ahy = pd.read_json(r"..\Scraper\data_clean\userProfile_AgusYudhoyono.json")
df_userprofile_ridwan = pd.read_json(r"..\Scraper\data_clean\userProfile_ridwankamil.json")

df_names = [df_userprofile_ganjar, df_userprofile_prabowo, df_userprofile_anies, df_userprofile_ahy, df_userprofile_ridwan]
df_string = ['ganjar', 'prabowo', 'anies', 'ahy', 'ridwan']

# =====================
# ===== Wordcloud =====
# =====================
print('Processing profile wordcloud images...')
# ___Join list as 1 string, and save wordcloud image___
for df in tqdm(range(len(df_names))):
    text_content = list(df_names[df]['clean_text_stem'])

    text_string = ''
    for elem in text_content:
        text_string = ' '.join([text_string, str(elem)])

    wordcloud = WordCloud(background_color='white').generate(text_string)

    # plot wordcloud
    plt.figure(figsize=(25,15))
    image = plt.imshow(wordcloud)

    # Hapus nilai axis
    plt.axis('off')
    # plt.show()
    # plt.imsave('wordcloud_{}.jpg'.format(df[3:]), arr=image)
    plt.savefig('./output/wordcloud_profile_{}.jpg'.format(df_string[df]))

print('\n'+ 'All wordcloud exported!')