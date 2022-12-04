# ===========================
# ===== Import Packages =====
# ===========================
import pandas as pd

from nltk.tokenize import word_tokenize
import gensim
from gensim.models.ldamodel import LdaModel
from gensim.models.coherencemodel import CoherenceModel

import pyLDAvis
import pyLDAvis.gensim_models

# =======================
# ===== Import Data =====
# =======================
df_ganjar = pd.read_csv(r"../Scraper\data_clean\userProfile_ganjarpranowo.csv")
df_prabowo = pd.read_csv(r"../Scraper\data_clean\userProfile_prabowo.csv")
df_anies = pd.read_csv(r"../Scraper\data_clean\userProfile_aniesbaswedan.csv")
df_ahy = pd.read_csv(r"../Scraper\data_clean\userProfile_AgusYudhoyono.csv")
df_ridwan = pd.read_csv(r"../Scraper\data_clean\userProfile_ridwankamil.csv")

df_names = [df_ganjar, df_prabowo, df_anies, df_ahy, df_ridwan]

# =====================
# ===== Functions =====
# =====================
# ___compute coherence value___
def compute_coherence_values(dictionary, corpus, texts, limit, start, step):
    coherence_values = []
    model_list = []
    for num_topics in range(start, limit, step):
        model = LdaModel(corpus=corpus, id2word=dictionary, num_topics=num_topics, iterations=100)
        model_list.append(model)
        coherencemodel = CoherenceModel(model=model, texts=texts, dictionary=dictionary, coherence='c_v')
        coherence_values.append(coherencemodel.get_coherence())
        
    return model_list, coherence_values

# ===========================
# ===== Preprocess Data =====
# ===========================
for df in df_names:
    df['text_token'] = df['clean_text_stem'].apply(lambda x: word_tokenize(x))

# ===========================
# ===== LDA with TF-IDF =====
# ===========================
for df in df_names:
    # ___membuat dictionary___
    dictionary = gensim.corpora.Dictionary(df['text_token'])

    # ___BOW corpus___
    bow_corpus = [dictionary.doc2bow(doc) for doc in df_ganjar['text_token']]

    # ___TF-IDF corpus___
    tfidf = gensim.models.TfidfModel(bow_corpus)
    corpus_tfidf = tfidf[bow_corpus]

    start=1
    limit=11
    step=1
    model_list, coherence_values = compute_coherence_values(dictionary, corpus=corpus_tfidf, 
                                                            texts=df_ganjar['text_token'],
                                                            start=start, limit=limit, step=step)