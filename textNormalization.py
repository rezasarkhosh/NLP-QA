# After scrapping textual data from tradingview we need to clean data (Text Normalization part).
import re
import string
from nltk.corpus import stopwords

def remove_emojis(text):
    emoji_pattern = re.compile(
        '['
        u'\U0001F600-\U0001F64F'  # Emoticons
        u'\U0001F300-\U0001F5FF'  # Symbols & Pictographs
        u'\U0001F680-\U0001F6FF'  # Transport & Map Symbols
        u'\U0001F700-\U0001F77F'  # Alchemical Symbols
        u'\U0001F780-\U0001F7FF'  # Geometric Shapes Extended
        u'\U0001F800-\U0001F8FF'  # Supplemental Arrows-C
        u'\U0001F900-\U0001F9FF'  # Supplemental Symbols and Pictographs
        u'\U0001FA00-\U0001FA6F'  # Chess Symbols
        u'\U0001FA70-\U0001FAFF'  # Symbols and Pictographs Extended-A
        u'\U00002702-\U000027B0'  # Dingbats
        u'\U000024C2-\U0001F251'
        ']+',
        flags=re.UNICODE
    )
    return emoji_pattern.sub(r'', text)

def normalize_text(text):

    text = text.lower()


   
    text = ' '.join(text.split())

   
    important_words = {'bitcoin', 'btc', 'ethereum', 'eth', 'crypto', 'pump' , 'dump' , 'btcusdt','ethusdt' , 'tether' , }

   
    text = text.translate(str.maketrans('', '', string.punctuation.replace('$', '').replace('%', '').replace('.', '').replace('!', '').replace('?', ''))).replace(')' , '')

    
    text = remove_emojis(text)

   
    custom_stop_words = set(stopwords.words('English')) - important_words

   
    text = ' '.join([word for word in text.split() if word not in custom_stop_words or word in important_words])

   
    text = re.sub(r'(?<=\d)[^\d\s](?=\d)', '-', text)

   
    text = re.sub(r'\.{2,}', '.', text)

   
    text = re.sub(r'(?<!\w)([.!?])', r'\1 ', text)  

   
    text = text.strip()

    return text


with open('data/BTC.txt', 'r') as file:
    btc_text = file.read()

normalized_text = normalize_text(btc_text)

with open('data/BTC_normalized.txt', 'w') as file:
    file.write(normalized_text)


 
with open('data/ETH.txt', 'r') as file:
    eth_text = file.read()

normalized_text = normalize_text(eth_text)

with open('data/ETH_normalized.txt', 'w') as file:
    file.write(normalized_text)

