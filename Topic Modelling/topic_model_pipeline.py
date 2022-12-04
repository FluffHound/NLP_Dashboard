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