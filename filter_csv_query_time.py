import csv
import re
import sys

# 輸入檔案和輸出檔案
input_file = input('target file name:')
output_file = 'filter_time.csv'
target_condition_value = input('query time, if don\'t have this, press enter to skip:')
# 如果沒有輸入，設為 False
if target_condition_value == '':
    target_condition_value = False
else:
    target_condition_value = int(target_condition_value)

target_str = input('target str, if don\'t have this, press enter to skip:')
# 如果沒有輸入，設為 False; 若有輸入則將其去掉大小寫以及將空白或換行字元統一變為一個空格
if target_str == '':
    target_str = False
else:
    target_str = re.sub('\s+', ' ', target_str).lower()


# 目標條件
target_condition_column = 'Query_time'

# 目標列的名稱（textPayload）
target_column = 'textPayload'

# 如果 target_str 或 target_condition_value 其中一個為 true 就進行 filter
# 若兩這皆為 False 就 print 請輸入數值，並結束程式
if target_str or target_condition_value:
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
            if target_column in row:
                # 分為 target_str and target_condition_value 都有值
                # target_str 有值，target_condition_value 無值
                # target_str 無值，target_condition_value 有值
                # target_str and target_condition_value 都無值，這四種情況
                # 都無值部分在 input arg 時就先濾掉

                # 首先 target_str and target_condition_value 都有值的情況
                if target_str and target_condition_value:
                    match = re.search(r'Query_time: ([0-9.]+)', row[target_column])
                    query_time = float(match.group(1))
                    
                    # 先檢查條件值是否超過目標值，如果沒超過就會直接檢查下一個 row ，不用在增加 search str 的 cost
                    if (query_time > target_condition_value):
                        match_str = re.search(target_str, row[target_column].replace('\s+', ' ').lower())
                        if match_str:
                            writer.writerow(row)
            

                # target_str 有值，target_condition_value 沒有值
                elif target_str and (target_condition_value == False):
                    match_str = re.search(target_str, row[target_column].replace('\s+', ' ').lower())
                    if match_str:
                        writer.writerow(row)
                # target_str 無值，target_condition_value 有值
                elif (target_str == False) and target_condition_value:
                    match = re.search(r'Query_time: ([0-9.]+)', row[target_column])
                    query_time = float(match.group(1))
                    if (query_time > target_condition_value):
                        writer.writerow(row)

# 若 target_str and target_condition_value 都無值
else:
    print('one of target_str and target_condition_value must input data!')


                



