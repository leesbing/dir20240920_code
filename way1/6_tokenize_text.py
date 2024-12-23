import pandas as pd
import nltk
from tqdm import tqdm

def tokenize_text(text):
    if pd.isna(text):
        return []
    return nltk.word_tokenize(str(text))

df = pd.read_csv(r"V:\20240920\way1\5_lemmatized_text_test.csv")

tokenized_text = [tokenize_text(text) for text in tqdm(df["lemmatized_text"], desc="Tokenizing text")]

df["tokenized_text"] = [' '.join(tokens) for tokens in tokenized_text]

df.to_csv(r"V:\20240920\way1\6_tokenized_text_test.csv", index=False)