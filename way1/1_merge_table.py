import pandas as pd

# 读取 DATA power文件
file_path = r"v:\20240920\DATA power pilot 3 WTOS Intersectional 11.17.2021 age effort iat.xlsx"  # Replace with the path to your file
df_datapower = pd.read_excel(file_path, sheet_name='DATA power pilot 3 WTOS Interse')



## 显示 DATA power 文件中 'ResponseID' 列中 NaN 的数量分布
print("\n --------- 1. DATA power 文件中 ResponseID 列中 NaN 的数量分布 ---------")

# 获取 DATA power 文件中 'ResponseID' 列中 NaN 的数量
nan_count = df_datapower['ResponseID'].isnull().sum()
print(f"列 'ResponseID' 中 NaN 的数量为: {nan_count}")

# 获取 DATA power 文件 'ResponseID' 列中 不是NaN 的数量
notna_count = df_datapower['ResponseID'].notna().sum()
print(f"列 'ResponseID' 中 非NaN 的数量为: {notna_count}")

# 获取 DATA power 文件中 'ResponseID' 列中的所有行元素的总数量
total_count = len(df_datapower['ResponseID'])
print(f"列 'ResponseID' 中的所有行元素的总数量为: {total_count}")

print("\n --------- 2. 清洗 DATA power 文件 ---------\n")
print("删除 'ResponseID' 列为空的行")
# 删除 'ResponseID' 列为空的行
df_datapower_cleaned = df_datapower.dropna(subset=['ResponseID'])

print("\n --------- 3. 检查 'ResponseID' 列是否有重复数据 ---------\n")
# 检查 'ResponseID' 列是否有重复数据，使用 any() 方法
if df_datapower_cleaned['ResponseID'].duplicated().any():
    print("DATA power文件中'ResponseID' 列存在重复数据")
else:
    print("DATA power文件中'ResponseID' 列没有重复数据")

# 计算 'ResponseID' 列存在重复数据的行数
duplicate_count = df_datapower_cleaned['ResponseID'].duplicated().sum()

# 输出结果
print(f"DATA power文件中'ResponseID' 列存在重复数据的行数为: {duplicate_count}")

# 读取 WTOS Letters 文件
file_path = r"v:\20240920\WTOS Letters to Congress Sept 21 2021 POWER PILOT 3 -head.xlsx"  # Replace with the path to your file
df_WTOS = pd.read_excel(file_path, sheet_name='Sheet1')

## 显示 WTOS Letters 文件中 'letter' 列中 NaN 的数量分布
print("\n --------- 1. WTOS Letters 文件中 letter 列中 NaN 的数量分布 ---------")

# 获取 WTOS Letters 文件中 'letter' 列中 NaN 的数量
nan_count = df_WTOS['letter'].isnull().sum()
print(f"列 'letter' 中 NaN 的数量为: {nan_count}")

# 获取 WTOS Letters 文件 'letter' 列中 不是NaN 的数量
notna_count = df_WTOS['letter'].notna().sum()
print(f"列 'letter' 中 非NaN 的数量为: {notna_count}")

# 获取 WTOS Letters 文件中 'letter' 列中的元素数量
total_count = len(df_WTOS['letter'])
print(f"列 'letter' 中元素的总数量为: {total_count}")

## 显示 WTOS Letters 文件中 'ResponseID' 列中 NaN 的数量分布
print("\n --------- 2. WTOS Letters 文件中 ResponseID 列中 NaN 的数量分布 ---------")

# 获取 WTOS Letters 文件中 'ResponseID' 列中 NaN 的数量
nan_count = df_WTOS['ResponseID'].isnull().sum()
print(f"列 'ResponseID' 中 NaN 的数量为: {nan_count}")

# 获取 WTOS Letters 文件 'ResponseID' 列中 不是NaN 的数量
notna_count = df_WTOS['ResponseID'].notna().sum()
print(f"列 'ResponseID' 中 非NaN 的数量为: {notna_count}")

# 获取 WTOS Letters 文件中 'ResponseID' 列中的元素数量
total_count = len(df_WTOS['ResponseID'])
print(f" WTOS Letters 文件的数据行总数为: {total_count}")


print("\n --------- 3. 清洗 WTOS Letters 文件  ---------")
# 删除 'ResponseID' 列为空的行
print("删除 'ResponseID' 列为空的行")
df_WTOS_cleaned = df_WTOS.dropna(subset=['ResponseID'])
# 删除 'Coder1' 列的值为 'CODER1' 的行
print("删除 'Coder1' 列的值为 'CODER1' 的行")
df_WTOS_cleaned = df_WTOS_cleaned[df_WTOS_cleaned['Coder1'] != 'CODER1']

print("\n --------- 4. 清洗后 WTOS Letters 文件中 ResponseID 列中 NaN 的数量分布 ---------")

# 获取 WTOS Letters 文件中 'ResponseID' 列中 NaN 的数量
nan_count = df_WTOS_cleaned['ResponseID'].isnull().sum()
print(f"列 'ResponseID' 中 NaN 的数量为: {nan_count}")

# 获取 WTOS Letters 文件 'ResponseID' 列中 不是NaN 的数量
notna_count = df_WTOS_cleaned['ResponseID'].notna().sum()
print(f"列 'ResponseID' 中 非NaN 的数量为: {notna_count}")

# 获取 WTOS Letters 文件中 'ResponseID' 列中的元素数量
total_count = len(df_WTOS_cleaned['ResponseID'])
print(f"清洗后 WTOS Letters 文件的数据行总数为: {total_count}")

# Merge DataFrames on 'ResponseID' column
df_merged = pd.merge(df_WTOS_cleaned, df_datapower_cleaned, on='ResponseID', how='outer')
# df_merged.tail(5)

## 显示 merge dataframe 中 'letter' 列中 NaN 的数量分布
print("\n --------- 2. merge dataframe 中 letter 列中 NaN 的数量分布 ---------")

# 获取 'letter' 列中 NaN 的数量
nan_count = df_merged['letter'].isnull().sum()
print(f"列 'letter' 中 NaN 的数量为: {nan_count}")

# 获取 'letter' 列中 不是NaN 的数量
notna_count = df_merged['letter'].notna().sum()
print(f"列 'letter' 中 非NaN 的数量为: {notna_count}")

# 获取 'letter' 列中的元素数量
total_count = len(df_merged['letter'])
print(f"列 'letter' 中元素的总数量为: {total_count}")

print("\n --------- end ---------")

## 显示 merge dataframe 中 'number_of_characters' 列中 NaN 的数量分布
print("\n --------- 3. merge dataframe 中 number_of_characters 列中 NaN 的数量分布 ---------")

# 获取 'number_of_characters' 列中 NaN 的数量
nan_count = df_merged['number_of_characters'].isnull().sum()
print(f"列 'number_of_characters' 中 NaN 的数量为: {nan_count}")

# 获取 'number_of_characters' 列中 不是NaN 的数量
notna_count = df_merged['number_of_characters'].notna().sum()
print(f"列 'number_of_characters' 中 非NaN 的数量为: {notna_count}")

# 获取 'number_of_characters' 列中的元素数量
total_count = len(df_merged['number_of_characters'])
print(f"列 'number_of_characters' 中行的总数量为: {total_count}")

# 获取 'number_of_characters' 列中的数值为0的行数量
total_count_nonzero = len(df_merged[df_merged['number_of_characters'] == 0])
print(f"列 'number_of_characters' 中数值为0的行数量为: {total_count_nonzero}")

# 获取 'number_of_characters' 列中的数值为非0的有效数字的行数量
valid_count = notna_count - total_count_nonzero
print(f"列 'number_of_characters' 中数值为 非0的有效数字 的行数量为: {valid_count}")

print("\n --------- end ---------")

# df_merged.tail(5)

from openpyxl import load_workbook

# Specify the file path
file_name1 = r"v:\20240920\way1\merged table v1.xlsx"

# Use ExcelWriter to save the DataFrame to a specific sheet
with pd.ExcelWriter(file_name1, engine='openpyxl', mode='w') as writer:
    df_merged.to_excel(writer, sheet_name='sheet1', index=True)