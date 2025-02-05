import re
import pandas as pd
from nltk.corpus import stopwords as sw
from nltk.stem import WordNetLemmatizer

def organize(lyrics):

    words = re.split('\s', lyrics)
    lower_text = [word.lower() for word in words]
    replaced = [re.sub('[\(\)\,\?\.\!\:\;]', '', word) for word in lower_text]
    stripped = [word.strip() for word in replaced]
    organized = [word for word in stripped if word]
    return organized

def sentence(lyrics):
    
    sentences = lyrics.splitlines()
    sentences = [sentence for sentence in sentences if sentence]
    return sentences

def tokenize(lyrics):
    """
    Converting lyrics into a list of  words
    """
    tokenized_text = re.split('\s|-|\'', lyrics)
    return tokenized_text

def normalize(lyrics, stopwords):
    """
    Setting all characters to lowercase, removing punctuation, and
    deleting stopwords
    """
    lower_text = [word.lower() for word in lyrics]
    no_punct = [re.sub('[^a-zA-Z]', '', word) for word in lower_text]
    stripped = [word.strip() for word in no_punct]
    words = [word for word in stripped if word not in stopwords]
    normalized = [word for word in words if word]
    return normalized

def lemmatize(lyrics, lemmatizer):
    """
    Changing variations of a word to the same word (e.g. walking, 
    walked, and walks are all forms of walk)
    """
    exceptions = ['us']
    lem_text = [lemmatizer.lemmatize(word) for word in lyrics if word not in exceptions]
    return lem_text
  
# Creating three sets of datasets to store different lyric structures
df = pd.read_csv('datasets/taylor-swift-song-lyrics.csv', index_col=0)
df2 = df.copy()
df3 = df.copy()

stopwords = [re.sub('[^\w\s]', '', word) for word in sw.words('english')]
stopwords.extend(['di', 'da', 'ey', 'yet', 'ooh', 'oh', 'yeah', 'like', 'la', 
                    'cause', 'never', 'know', 'would', 'could', 'wanna', 'gonna', 'ah',
                    'eeh', 'e', 'na', 'ha', 'ra', 'aah', 'mmm', 'ho', 'hey', 'id'])
                    
lemmatizer = WordNetLemmatizer()

df['lyrics'] = df['lyrics'].apply(lambda x: tokenize(x))
df['lyrics'] = df['lyrics'].apply(lambda x: normalize(x, stopwords))
df['lyrics'] = df['lyrics'].apply(lambda x: lemmatize(x, lemmatizer))
df.to_csv('datasets/cleaned-lyrics.csv')

df2['lyrics'] = df2['lyrics'].apply(lambda x: organize(x))
df2.to_csv('datasets/original-lyrics.csv')

df3['lyrics'] = df3['lyrics'].apply(lambda x: sentence(x))
df3.to_csv('datasets/sentence-lyrics.csv')