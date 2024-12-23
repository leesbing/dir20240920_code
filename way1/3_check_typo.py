import pandas as pd
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
import language_tool_python
import multiprocessing

# 获取 CPU 的内核数量
cpu_count = multiprocessing.cpu_count()

# 初始化 LanguageTool,连接到本地服务器
# language_tool = language_tool_python.LanguageTool('en-us')
language_tool = language_tool_python.LanguageTool('en-us', remote_server='http://localhost:8081/') 

# 初始化 LanguageTool
# language_tool = language_tool_python.LanguageTool('en-us')

def correct_spelling(text):
    """
    修正文本中的拼写和语法错误
    """
    matches = language_tool.check(text)
    corrected_text = language_tool.correct(text)  # 使用 correct 方法修正文本
    return corrected_text.lower()  # 返回小写形式的修正文本

def correct_array_with_threads(text_array):
    """
    使用多线程修正文本数组
    """
    corrected_results = [None] * len(text_array)
    with ThreadPoolExecutor(max_workers=cpu_count) as executor:
        futures = {executor.submit(correct_spelling, str(text)): idx for idx, text in enumerate(text_array)}
        for future in tqdm(as_completed(futures), total=len(futures), desc="Correcting typos"):
            idx = futures[future]
            try:
                corrected_results[idx] = future.result()
            except Exception as e:
                print(f"Error processing text at index {idx}: {e}")
                corrected_results[idx] = text_array[idx]  # 如果出错，保留原始文本

    return corrected_results

# 读取 CSV 文件
df = pd.read_csv(r"V:\20240920\way1\2_processed_data.csv")

# 获取需要处理的文本列
text = df["processed_text"].tolist()  # 将 Pandas Series 转换为列表

# 使用多线程修正文本
result = correct_array_with_threads(text)

# 将修正后的结果写回 DataFrame
df["processed_text"] = result  # 直接赋值给列

# 保存到新的 CSV 文件
df.to_csv(r"V:\20240920\way1\3_correct_text_test.csv", index=False)

# 关闭 LanguageTool
language_tool.close()