import pandas as pd
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from tqdm import tqdm

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('averaged_perceptron_tagger')

lemmatizer = WordNetLemmatizer()

def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN

def lemmatize_text(text):
    if pd.isna(text):
        return ""  
    text = str(text)  
    words = nltk.word_tokenize(text)
    pos_tags = nltk.pos_tag(words)
    lemmatized_words = [lemmatizer.lemmatize(word, get_wordnet_pos(tag)) for word, tag in pos_tags]
    return ' '.join(lemmatized_words)

df = pd.read_csv(r"V:\20240920\way1\4_expanded_text_test.csv")

lemmatized_text = [lemmatize_text(text) for text in tqdm(df["processed_text"], desc="Lemmatizing text")]

df["lemmatized_text"] = lemmatized_text

df.to_csv(r"V:\20240920\way1\5_lemmatized_text_test.csv", index=False)