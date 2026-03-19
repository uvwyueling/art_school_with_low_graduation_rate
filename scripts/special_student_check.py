import pandas as pd
import hashlib
import numpy as np
import sqlite3

df_raw_grad = pd.read_csv("/Users/juri/Happy_coding/art_school_with_low_graduation_rate/data/raw/raw_graduation.csv", encoding="utf-8-sig")

# 改变数据类型
def cast_types(df, col_to_str=None):
    for col in col_to_str:
        df[col]=df[col].astype('str')
    return df
df_raw_grad_stage = cast_types(df_raw_grad, col_to_str=['学号', '年级', '班级'])

# 学生学号的前四位数即 入学年份
df_raw_grad_stage['入学年份'] = df_raw_grad_stage['学号'].str[:4]

# ’入学年份‘ 和 ’年级‘ 字段不一致的同学学籍异常，往往是休学或降级。
df_raw_grad_stage['入学年份和年级是否一致'] =  (df_raw_grad_stage['入学年份'] == df_raw_grad_stage['年级'])

# 快速确定学籍异常同学规模
result = pd.DataFrame({
    '人数': df_raw_grad_stage['入学年份和年级是否一致'].value_counts(),
    '百分比': df_raw_grad_stage['入学年份和年级是否一致'].value_counts(normalize=True).map(lambda n: f'{n:.2%}')
})

print(result)

# 发现17人，因此导出名单，手工回到教务系统逐一检查学籍异常细节
special_students = df_raw_grad_stage[
    df_raw_grad_stage['入学年份和年级是否一致'] == False][['学号', '姓名', '年级', '入学年份', '毕业年份']]  

special_students.to_csv('/Users/juri/Happy_coding/art_school_with_low_graduation_rate/data/raw/to_verify_17students.csv', index=False, encoding='utf-8-sig')