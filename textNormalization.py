# After scrapping textual data from tradingview we need to clean data (Text Normalization part).
import re 
import string
from nltk.corpus import stopwords


def normalize_text(text):

    text = text.lower()
    text= ' '.join(text.split())
    text = text.translate(str.maketrans('', '', string.punctuation.replace('$', '').replace('%', '')))

    stop_words = set(stopwords.words('English'))
    text = ' '.join([word for word in text.split() if word not in stop_words])

    text = re.sub(r'\.{2,}', '.', text)
    text = text.replace('\n', ' ').strip()

    return text

with open('data/BTC.txt', 'r') as file:
    btc_text = file.read()

normalized_text = normalize_text(btc_text)

with open('data/BTC_normalized.txt', 'w') as file:
    file.write(normalized_text)

    

with open('data/ETH.txt', 'r') as file:
    ETH_text = file.read()

normalized_text = normalize_text(ETH_text)

with open('data/ETH_normalized.txt', 'w') as file:
    file.write(normalized_text)
    
