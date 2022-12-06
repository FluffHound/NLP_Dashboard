# ===========================
# ===== Import Packages =====
# ===========================
import pandas as pd
from tqdm import tqdm

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation

import pyLDAvis
import pyLDAvis.sklearn

# =======================
# ===== Import Data =====
# =======================
df_ganjar = pd.read_csv(r"../Scraper\data_clean\userProfile_ganjarpranowo.csv")
df_prabowo = pd.read_csv(r"../Scraper\data_clean\userProfile_prabowo.csv")
df_anies = pd.read_csv(r"../Scraper\data_clean\userProfile_aniesbaswedan.csv")
df_ahy = pd.read_csv(r"../Scraper\data_clean\userProfile_AgusYudhoyono.csv")
df_ridwan = pd.read_csv(r"../Scraper\data_clean\userProfile_ridwankamil.csv")

df_names = [df_ganjar, df_prabowo, df_anies, df_ahy, df_ridwan]
df_string = ['ganjar', 'prabowo', 'anies', 'ahy', 'ridwan']

# =============================
# ===== Initialize TF-IDF =====
# =============================
tfidf_vectorizer = TfidfVectorizer()

for df in tqdm(range(len(df_names))):
    # ___apply TF-IDF___
    dtm_tfidf = tfidf_vectorizer.fit_transform(list(df_names[df]['clean_text_stem']))

    # ___apply LDA___
    lda_tfidf = LatentDirichletAllocation(n_components=10)
    lda_tfidf.fit(dtm_tfidf)

    # ___export HTML___
    data = pyLDAvis.sklearn.prepare(lda_tfidf, dtm_tfidf, tfidf_vectorizer)
    pyLDAvis.save_html(data, './output/lda_{}.html'.format(df_string[df]))