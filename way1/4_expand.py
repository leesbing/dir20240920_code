import pandas as pd
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
import contractions
import re
import json

with open(r"V:\20240920\github\abbreviations.json", 'r', encoding='utf-8') as f:
    abbreviation_mapping = json.load(f)

def expand_abbreviations(text):

    text = contractions.fix(text)

    for abbr, full_form in abbreviation_mapping.items():
        text = re.sub(r'\b' + re.escape(abbr) + r'\b', full_form, text, flags=re.IGNORECASE)
    return text


df = pd.read_csv(r"V:\20240920\way1\3_correct_text_test.csv")
text = df["processed_text"]

# 获取 CPU 的内核数量
cpu_count = multiprocessing.cpu_count()
thread_count = cpu_count

expanded_text = [None] * len(text)
with ThreadPoolExecutor(max_workers=thread_count) as executor:
    futures = {executor.submit(expand_abbreviations, str(t)): idx for idx, t in enumerate(text)}
    for future in tqdm(as_completed(futures), total=len(futures), desc="Expanding abbreviations", mininterval=0.5):
        idx = futures[future]
        try:
            expanded_text[idx] = future.result()
        except Exception as e:
            expanded_text[idx] = text.iloc[idx]

df["processed_text"] = expanded_text

df.to_csv(r"V:\20240920\way1\4_expanded_text_test.csv", index=False)