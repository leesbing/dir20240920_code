# -*- coding: utf-8 -*-
# Requires: pandas, nltk (pip install pandas nltk)
# NLTK: Make sure to download 'stopwords' with nltk.download('stopwords', quiet=True)

import pandas as pd
import string
import re
from collections import Counter
import nltk
from nltk.corpus import stopwords
import unicodedata

nltk.download('stopwords', quiet=True)

def preprocess_text(text):
    if pd.isna(text) or text.strip() == '':
        return "", Counter(), 0

    punctuation_count = Counter(char for char in str(text) if char in string.punctuation)

    text = text.lower()
    text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')

    text = remove_unwanted_content(text)
    text = remove_punctuation_and_special_chars(text)
    text = remove_stopwords(text)

    words = text.split()
    return text, punctuation_count, len(words)

def remove_unwanted_content(text):
    patterns = [
        r'\([^)]*\)',  # Remove parenthetical notes
        r'\b(?:dear\s+senator|dear|hello|hi|your honorable whomever|to whom it may concern|to senator).*?:\s*',  # Remove greetings
        r'\b(?:sincerely|best regards|regards|yours truly|best|thank you).*$',  # Remove closings
        r'\b(?:\d{1,2}[-/]\d{1,2}[-/]\d{2,4}|\w+\s+\d{1,2},?\s+\d{4})\b',  # Remove dates
        r'\b(?:january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{1,2},?\s+\d{4}\b',  # Remove month-based dates
        r'\b(?:dear|hello|hi)\s+(?:senator|representative|mr\.?|mrs\.?|ms\.?).*?[\s,:]',  # Remove additional greetings
        r'\n[A-Z\s]+$'  # Remove remaining lines that are just names
    ]
    for pattern in patterns:
        text = re.sub(pattern, '', text, flags=re.IGNORECASE | re.MULTILINE)
    return text

def remove_punctuation_and_special_chars(text):
    return re.sub(r'[^\w\s]', '', text)

def remove_stopwords(text):
    stop_words = set(stopwords.words('english'))
    words = text.split()
    return ' '.join([word for word in words if word not in stop_words])

def handle_null_values(df):
    null_counts = df.isnull().sum().to_frame(name='null_count')
    null_counts['null_percentage'] = (null_counts['null_count'] / len(df)) * 100

    print("Null values in each column:")
    print(null_counts)

    total_rows_before = len(df)
    df_clean = df.dropna(subset=['letter'])
    total_rows_after = len(df_clean)
    removed_rows = total_rows_before - total_rows_after

    print(f"\nTotal number of rows before removal: {total_rows_before}")
    print(f"Number of rows removed due to null values in 'letter' column: {removed_rows}")
    print(f"Total number of rows after removal: {total_rows_after}")

    return df_clean, null_counts, removed_rows

def process_data(file_path):
    try:
        # 读取 Excel 文件
        df = pd.read_excel(file_path, sheet_name='sheet1')

        ## Task1: replace the specific mistake characters
        #详见《 letter列文本中的乱码及处理方法.xlsx》 
        replacements = {
            '‚Äô': "'",
            '‚äô': "'",
            '√©': " ",
            'Äì¬†': " ",
            '‚Äú': "\"",
            '‚Äù': "\'",
            '‚Äî': "--",
            '‚Ä¶': " ",
            '√≥': "o"
        }
        for old, new in replacements.items():
            df['letter'] = df['letter'].str.replace(old, new, regex=False)

        df, null_counts, removed_rows = handle_null_values(df)

        df['row_null_count'] = df.isnull().sum(axis=1)
        df['null_columns'] = df.apply(lambda row: ', '.join(row.index[row.isnull()]), axis=1)
        df['processed_text'], df['punctuation_count'], df['word_count'] = zip(*df['letter'].apply(preprocess_text))

        # Handle short letters - just mark
        mean_word_count = df['word_count'].mean()
        std_word_count = df['word_count'].std()
        df['is_short'] = df['word_count'] < (mean_word_count - std_word_count)

        # Fill missing values for categorical and numerical columns
        df['coding1'] = df['coding1'].fillna('unknown')
        df['coding2'] = df['coding2'].fillna('unknown')
        df['coding3'] = df['coding3'].fillna('unknown')
        df['word_count'] = df['word_count'].fillna(df['word_count'].mean())
        df['processed_text'] = df['processed_text'].fillna('')

        columns = list(df.columns)
        punctuation_index = columns.index('punctuation_count')
        columns.insert(punctuation_index + 1, columns.pop(columns.index('row_null_count')))
        columns.insert(punctuation_index + 2, columns.pop(columns.index('null_columns')))
        df = df[columns]

        return df
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

# Main execution
if __name__ == "__main__":
    file_path = r"V:\20240920\way1\1_merged table v1.xlsx"
    result_df = process_data(file_path)
    if result_df is not None:
        output_path = r"V:\20240920\way1\2_processed_data.csv"
        result_df.to_csv(output_path, index=False)
        print(f"\nPreprocessing complete. Processed data saved to '{output_path}'.")
        print("\nFirst few rows of the processed data:")
        print(result_df[['letter', 'processed_text', 'punctuation_count', 'row_null_count', 'null_columns', 'word_count', 'is_short']].head())