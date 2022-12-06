# ===========================
# ===== Import Packages =====
# ===========================
import pandas as pd
from tqdm import tqdm

from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification

# =======================
# ===== Import Data =====
# =======================
df_hashtag_ganjar = pd.read_csv(r"..\Scraper\data_clean\hashtag_ganjarpranowofor2024.csv")
df_hashtag_prabowo = pd.read_csv(r"..\Scraper\data_clean\hashtag_prabowo.csv")
df_hashtag_anies = pd.read_csv(r"..\Scraper\data_clean\hashtag_AniesPresiden2024.csv")
df_hashtag_ahy = pd.read_csv(r"..\Scraper\data_clean\hashtag_AHY.csv")
df_hashtag_ridwan = pd.read_csv(r"..\Scraper\data_clean\hashtag_RidwanKamil.csv")

df_mention_ganjar = pd.read_csv(r"..\Scraper\data_clean\userMention_@ganjarpranowo.csv")
df_mention_prabowo = pd.read_csv(r"..\Scraper\data_clean\userMention_@prabowo.csv")
df_mention_anies = pd.read_csv(r"..\Scraper\data_clean\userMention_@aniesbaswedan.csv")
df_mention_ahy = pd.read_csv(r"..\Scraper\data_clean\userMention_@AgusYudhoyono.csv")
df_mention_ridwan = pd.read_csv(r"..\Scraper\data_clean\userMention_@ridwankamil.csv")

# ___Concat Dataframe___
df_ganjar = pd.concat([df_hashtag_ganjar, df_mention_ganjar], ignore_index=True)
df_prabowo = pd.concat([df_hashtag_prabowo, df_mention_prabowo], ignore_index=True)
df_anies = pd.concat([df_hashtag_anies, df_mention_anies], ignore_index=True)
df_ahy = pd.concat([df_hashtag_ahy, df_mention_ahy], ignore_index=True)
df_ridwan = pd.concat([df_hashtag_ridwan, df_mention_ridwan], ignore_index=True)

df_names = [df_ganjar, df_prabowo, df_anies, df_ahy, df_ridwan]
df_string = ['ganjar', 'prabowo', 'anies', 'ahy', 'ridwan']

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

    pos_df.to_csv('./output/pos_{}.csv'.format(df_string[df]))
    neu_df.to_csv('./output/neu_{}.csv'.format(df_string[df]))
    neg_df.to_csv('./output/neg_{}.csv'.format(df_string[df]))

print('ALL DONE!')

# ===========================
# ===== Import Packages =====
# ===========================