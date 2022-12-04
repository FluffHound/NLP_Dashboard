# ===========================
# ===== Import Packages =====
# ===========================
import pandas as pd

from nltk.tokenize import word_tokenize
import gensim
from gensim.models.ldamodel import LdaModel
from gensim.models.coherencemodel import CoherenceModel

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation

import pyLDAvis
import pyLDAvis.sklearn

# =======================
# ===== Import Data =====
# =======================
df = pd.read_csv(r"../Scraper\data_clean\userProfile_ganjarpranowo.csv")
df = df.dropna().reset_index()

tf_vectorizer = CountVectorizer()

docs_raw = list(df['clean_text_stem'])
print(docs_raw)

dtm_tf = tf_vectorizer.fit_transform(docs_raw)
tfidf_vectorizer = TfidfVectorizer(**tf_vectorizer.get_params())
dtm_tfidf = tfidf_vectorizer.fit_transform(docs_raw)

# for TF DTM
lda_tf = LatentDirichletAllocation(n_components=20, random_state=0)
lda_tf.fit(dtm_tf)
# for TFIDF DTM
lda_tfidf = LatentDirichletAllocation(n_components=20, random_state=0)
lda_tfidf.fit(dtm_tfidf)

data = pyLDAvis.sklearn.prepare(lda_tf, dtm_tf, tf_vectorizer)
pyLDAvis.save_html(data, 'lda-gensim-tfidf.html')