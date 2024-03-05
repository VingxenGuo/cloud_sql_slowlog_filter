import csv
import re

# 輸入檔案和輸出檔案
input_file = 'downloaded-logs-20240305-143140.csv'
output_file = 'filter_time_vp.csv'

# 目標條件
target_condition_column = 'Query_time'
target_condition_value = 0
target_str = "SELECT \
    t.TABLE_SCHEMA AS TableSchema,\
    t.TABLE_NAME AS TableName,\
    t.TABLE_TYPE AS TableType,\
    t.TABLE_COMMENT AS TableDescription"

# 目標列的名稱（textPayload）
target_column = 'textPayload'

# 打開 CSV 檔案進行讀取和寫入
with open(input_file, 'r', newline='', encoding='utf-8') as csv_input, \
        open(output_file, 'w', newline='', encoding='utf-8') as csv_output:

    # 創建 CSV 讀寫物件
    reader = csv.DictReader(csv_input)
    fieldnames = reader.fieldnames

    # 確保輸出的 CSV 檔案包含相同的欄名
    writer = csv.DictWriter(csv_output, fieldnames=fieldnames)
    writer.writeheader()

    # 遍歷每一行，篩選符合條件的行
    for row in reader:
        # 檢查目標列是否存在
        if target_column in row:
            # 從 textPayload 中提取 Query_time
            match = re.search(r'Query_time: ([0-9.]+)', row[target_column])
            if target_str:
                match_str = re.search(target_str, row[target_column])
            
            if match:
                query_time = float(match.group(1))
                
                # 檢查條件值是否超過目標值
                if query_time > target_condition_value:
                    # print(query_time)
                    writer.writerow(row)

