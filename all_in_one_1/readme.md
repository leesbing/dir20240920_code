### 文件《1_merge_table.ipynb》
- 输入 DATA power 和 WTOS 文件
- 清洗 DATA power 和 WTOS 文件 
- 用'ResponseID'列，合并 DATA power 和 WTOS 文件 
- 输出结果 《1_merged table v1.xlsx》

### 文件《2_data_preprocessing_BERT.ipynb》
- 输入文件《1_merged table v1.xlsx》
- 矫正乱字符，
- 另外新增了几列，用于统计
- 输出结果 《2_processed_data_BERT.csv》

### 文件《3_add_emotion_detection.ipynb》
- 输入文件《2_processed_data_BERT.csv》
- 新建28列，保存emotion
- 输出结果《3_add_emotion.csv》

### 文件《4_embedding(stella).ipynb》
- 输入文件《3_add_emotion.csv》
- 对`letter`列的内容做embedding
- 输出结果《4_embeddings_stella.npy》

### 文件《5_varimax_themes_analysis.ipynb》
- 输入文件《3_add_emotion.csv》 和 《4_embeddings_stella.npy》
- PCA + Varimax rotation
- 新建Components数量的列，保存每个`letter`对应的 rotated score ， 输出结果《5_add_rotated_scores.csv》
- 方便 themes analysis ， 输出结果《5_top_letters_per_rotated_component.csv》
