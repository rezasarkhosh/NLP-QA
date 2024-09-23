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

    
    unwanted_words = {'hi', 'hello', 'hey', 'traders', 'bye'}
    important_words = {'bitcoin', 'btc', 'ethereum', 'eth', 'crypto', 'pump', 'dump', 'btcusdt', 'ethusdt', 'tether'}

    
    text = text.translate(str.maketrans('', '', string.punctuation.replace('$', '').replace('%', '').replace('.', '').replace('!', '').replace('?', ''))).replace(')', '')

    
    text = remove_emojis(text)

    
    custom_stop_words = set(stopwords.words('English')) - important_words
    
    all_unwanted_words = custom_stop_words.union(unwanted_words)

    text = ' '.join([word for word in text.split() if word not in all_unwanted_words])

    
    text = re.sub(r'(?<=\d)[^\d\s](?=\d)', '-', text)

    
    text = re.sub(r'\.{2,}', '.', text)

    
    text = re.sub(r'(?<!\w)([.!?])', r'\1 ', text)

    
    text = text.strip()

    return text

def process_file(input_file, output_file):
    
    with open(input_file, 'r') as file:
        text = file.read()

    analyses = text.split("___")

    with open(output_file, 'w') as f:
        for analysis in analyses:
            normalized_analysis = nصormalize_text(analysis.strip())  
            if normalized_analysis:  
                f.write(normalized_analysis + "\n\n") 


process_file('data/BTC.txt', 'data/BTC_normalized.txt')
process_file('data/ETH.txt', 'data/ETH_normalized.txt')
