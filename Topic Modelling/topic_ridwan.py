# =======================
# ===== Import Data =====
# =======================
df = pd.read_csv(r"../Scraper\data_clean\userProfile_ridwankamil.csv")

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
df['text_token'] = df['clean_text_stem'].apply(lambda x: word_tokenize(str(x)))

# ===========================
# ===== LDA with TF-IDF =====
# ===========================
print('Creating topic model for Ridwan')
# ___membuat dictionary___
dictionary = gensim.corpora.Dictionary(df['text_token'])

# ___BOW corpus___
bow_corpus = [dictionary.doc2bow(doc) for doc in df['text_token']]

# ___TF-IDF corpus___
tfidf = gensim.models.TfidfModel(bow_corpus)
corpus_tfidf = tfidf[bow_corpus]

# ___hitung nilai coherence___
start=1
limit=11 # Max 10 topic
step=1
model_list, coherence_values = compute_coherence_values(dictionary, corpus=corpus_tfidf, 
                                                        texts=df['text_token'],
                                                        start=start, limit=limit, step=step)
# ___LDA model___
model = LdaModel(corpus=corpus_tfidf, id2word=dictionary, num_topics=(coherence_values.index(max(coherence_values)) + 1))

# ___save model___
data = pyLDAvis.gensim_models.prepare(model, corpus_tfidf, dictionary)
pyLDAvis.save_html(data, './output/lda_ridwan.html')