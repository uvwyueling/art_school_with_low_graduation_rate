# region 1. 加载库、初始化数据
import pandas as pd
import hashlib
import numpy as np
import sqlite3

df_stg_reassign = pd.read_csv("/Users/juri/Happy_coding/art_school_with_low_graduation_rate/data/stage/stage_reassign.csv", encoding="utf-8-sig")
df_2014_1y_gpa = pd.read_csv("/Users/juri/Happy_coding/art_school_with_low_graduation_rate/data/raw/raw_2014_first_year_GPA.csv", encoding="utf-8-sig")
df_raw_grad = pd.read_csv("/Users/juri/Happy_coding/art_school_with_low_graduation_rate/data/raw/raw_graduation.csv", encoding="utf-8-sig")
df_raw_last3y_gpa = pd.read_csv("/Users/juri/Happy_coding/art_school_with_low_graduation_rate/data/raw/raw_last3y_gpa.csv", encoding="utf-8-sig")
df_17students = pd.read_csv("/Users/juri/Happy_coding/art_school_with_low_graduation_rate/data/stage/to_verify_17students.csv", encoding="utf-8-sig")
df_patch_last3y_gpa = pd.read_csv("/Users/juri/Happy_coding/art_school_with_low_graduation_rate/data/raw/patch_last3y_gpa.csv", encoding="utf-8-sig")
# endregion

# region 2. 定义可复用的清洗函数
    # 2.1 清理字符串空格 strip_whitespace() 
def strip_whitespace(df):
    string_cols = df.select_dtypes(include='object').columns
    for col in string_cols:
        df[col] = df[col].str.strip()
    return df    

    # 2.2：剔除非设计类的学生数据 exclude_other_major()
def exclude_other_major(df):
    df = df[~(df['专业'].str.contains('美术学|专升本|建筑学', na=False) )].reset_index(drop=True)
    return df

    # 2.3：缺失值处理 handle_missing_values()
def handle_missing_values(df):
    for col in df.columns:
        null_n = df[col].isnull().sum()
        if null_n == 0:
            print(f"✅ {col}列未发现缺失值")
        else:    
            print(f"⚠️ {col}列存在{null_n}个缺失值，{df[df[col].isnull()]}")

    # 2.4：确认无重复记录 validate_uniqueness()
def validate_uniqueness(df):
    duplicate_df = df[df.duplicated(subset = ['学号'], keep=False)]

    if duplicate_df.empty:
        print("✅ 未发现学号重复的行")
    else:
        print("⚠️ 发现学号重复！详情如下：")
        print(duplicate_df)    

    # 2.5：数据类型转换 cast_types()
def cast_types(df, col_to_str=None):
    for col in col_to_str:
        df[col]=df[col].astype('str')
    return df
# 调用的时候这样用：cast_types(df_raw_grad, col_to_str=['学号', '年级', '班级'])

    # 2.6：学号脱敏 mask_student_id
def mask_student_id(df, id_col='uid'):
    df[id_col] = df[id_col].apply(lambda x: hashlib.sha256(x.encode()).hexdigest())
    return df
# endregion


# region 3. 调用函数来清洗四个数据集
    # 3.1 处理 stage_reassign  (df_stg_reassign 备注：人工录入数据，潜在的问题较多）
print(df_stg_reassign.head())

df_stg_reassign = strip_whitespace(df_stg_reassign)
handle_missing_values(df_stg_reassign)
validate_uniqueness(df_stg_reassign)

#剔除三位休学同学的专业分流信息（“最终专业”列是空值），因为大一学年后他们休学了
df_stg_reassign = df_stg_reassign[~(df_stg_reassign['最终专业'].isnull() )].reset_index(drop=True)

df_stg_reassign_ready = cast_types(df_stg_reassign, col_to_str=['学号','所在班级','年级'])

# 追加：逻辑判断、新增is_reassign 列  
df_stg_reassign_ready['is_reassign'] = (df_stg_reassign_ready['最终专业'] != df_stg_reassign_ready['拟分流专业第一志愿'])

print(df_stg_reassign_ready.head())  
print(df_stg_reassign_ready.dtypes) 

# 验证三位休学同学的数据是否已剔除
drop_ok = (df_stg_reassign_ready['最终专业'].isnull() )
print(f"  三位休学同学的数据记录：{'✅ 已成功删除' if not drop_ok.any() else '❌ 未删除，请复查'}")

# 作为清洗单个数据集的分割线
print("=" * 40)
print("stage_reassign.csv 2015-2017即学生的专业分流志愿表 已清洗完毕")
print("=" * 40)

    # 3.2 处理 raw_2014_first_year_GPA  (df_2014_1y_gpa)
print(df_2014_1y_gpa.head())

df_2014_1y_gpa = strip_whitespace(df_2014_1y_gpa)
df_2014_1y_gpa = exclude_other_major(df_2014_1y_gpa)
handle_missing_values(df_2014_1y_gpa)
validate_uniqueness(df_2014_1y_gpa)
df_2014_1y_gpa_ready = cast_types(df_2014_1y_gpa, col_to_str=['学号','班级','年级'])

print(df_2014_1y_gpa_ready.head())  
print(df_2014_1y_gpa_ready.dtypes) 

# 作为清洗单个数据集的分割线
print("=" * 40)
print("raw_2014_first_year_GPA.csv 已清洗完毕")
print("=" * 40)

    # 3.3 处理 raw_graduation    (df_raw_grad)
# 追加步骤:补全零星缺失值（班级列）
# 步骤5：新增 grad_status 列                          
# 追加步骤: 处理17位年级异常同学的 grad_status 数据           
    # 降级学生的“年级”字段比实际少1，所以需要从 `df_17students` 表中筛选出 “设计系的降级学生”（该部分学生已前期在excel中根据教务系统记录标注完成）    

print(df_raw_grad.head())

df_raw_grad = strip_whitespace(df_raw_grad)
df_raw_grad = exclude_other_major(df_raw_grad)
handle_missing_values(df_raw_grad)
validate_uniqueness(df_raw_grad)

# 追加步骤: 补全零星缺失的班级信息
df_raw_grad.loc[df_raw_grad["班级"].isnull(), "班级"] = 20150623.0

# 简单计算后得到临时列:修读年限(study_yrs)
df_raw_grad["study_yrs"] = df_raw_grad["毕业年份"] - df_raw_grad["年级"]  # 临时列

# 追加步骤：给降级的设计系学生的“修读年限”字段+1
# 提取目标同学的学号，存成一个列表
students_to_fix = df_17students.loc[df_17students['是否需要手动校准在校年限'] == "是", '学号']

# 在 df_raw_grad 里找到这些人，给 study_yrs +1
df_raw_grad.loc[df_raw_grad['学号'].isin( students_to_fix ), 'study_yrs'] += 1

# 综合上面两行 "study_yrs"的数值，进行逻辑判断，得到 grad_status 列 
conditions = [
    df_raw_grad["study_yrs"] == 4,
    df_raw_grad["study_yrs"] == 5,
    df_raw_grad["study_yrs"] == 6
]
results = ['四年正常','五年异常','六年异常']
df_raw_grad['grad_status'] = np.select(conditions, results, default='未毕业')
df_raw_grad_stage = df_raw_grad.drop(columns=["study_yrs"]) #删除临时列

df_raw_grad_ready = cast_types(df_raw_grad_stage, col_to_str=['学号','班级','年级','毕业年份'])

print(df_raw_grad_ready.head())
print(df_raw_grad_ready.dtypes)

# 验证零星缺失值（班级列）是否已修复
print(df_raw_grad_ready.loc[df_raw_grad_ready["学号"]=="2015062135"])

# 验证降级学生的修读年限是否已修复
print(df_raw_grad_ready.loc[df_raw_grad_ready["学号"].isin(students_to_fix.astype(int).astype(str))])

# 作为清洗单个数据集的分割线
print("=" * 40)
print("raw_graduation.csv 已清洗完毕")
print("=" * 40)

    # 3.4 处理 raw_last3y_gpa   (df_raw_last3y_gpa)
# 追加步骤：教务系统故障，一开始批量导出gpa数据的时候两位降级学生的数据缺失，现在把额外的表补上    

# 把两个同学的成绩表和原表合并到一起
df_raw_last3y_gpa_temp = pd.concat([df_raw_last3y_gpa , df_patch_last3y_gpa], ignore_index=True)

df_raw_last3y_gpa_temp = strip_whitespace(df_raw_last3y_gpa_temp)
df_raw_last3y_gpa_temp = exclude_other_major(df_raw_last3y_gpa_temp)
handle_missing_values(df_raw_last3y_gpa_temp)
validate_uniqueness(df_raw_last3y_gpa_temp)
df_raw_last3y_gpa_ready = cast_types(df_raw_last3y_gpa_temp, col_to_str=['学号','班级','年级'])

print(df_raw_last3y_gpa_ready.head())
print(df_raw_last3y_gpa_ready.dtypes)

# 作为清洗单个数据集的分割线
print("=" * 40)
print("raw_last3y_gpa.csv 已清洗完毕")
print("=" * 40)
# endregion


# region 4. 搭建数据库骨架
    # 4.1 dim_student 表
# uid                          ← 来自 df_raw_grad_ready "学号" 字段
# year_1_class_num             ← 来自 df_2014_1y_gpa_ready “班级”字段 + df_stg_reassign_ready “所在班级” 字段
# grad_class_num               ← 来自 df_raw_grad_ready “班级” 字段
# enroll_year                  ← 来自 df_raw_grad_ready “年级” 字段
# grad_status                  ← 来自 df_raw_grad_ready “grand_status” 字段  

temp_2014 = df_2014_1y_gpa_ready[['学号','班级']]
temp_reassign = df_stg_reassign_ready[['学号','所在班级']]

temp_2014 = temp_2014.rename(columns={'班级':'大一班级'})
temp_reassign = temp_reassign.rename(columns={'所在班级':'大一班级'})

y1_class_num_temp = pd.concat([temp_2014 , temp_reassign], ignore_index=True)

temp_dim_student = pd.merge(df_raw_grad_ready , y1_class_num_temp , on='学号' , how='inner')
# inner join后被排除了17位学籍异常的学生，经逐一探查，发现他们不属于本项目的分析对象，具体情况请参考 `data_dictionary.md` 文件

print(f"df_raw_grad_ready 行数：{len(df_raw_grad_ready)}")  
print(f"y1_class_num_temp 行数：{len(y1_class_num_temp)}")  
print(temp_dim_student.head())
print(f"合并后行数：{len(temp_dim_student)}")  

stage_dim_student = temp_dim_student.drop(columns=['姓名', '是否在校','是否已毕业','毕业年份'])

# 删去“年级”列数据最后的“.0” (因为原始类型是float，cast_types() 把它转成字符串后保留了 .0)
stage_dim_student['班级'] = stage_dim_student['班级'].str[:-2]

# 修改列名
temp_dim_student = stage_dim_student.rename(columns={'学号': 'uid','大一班级': 'year_1_class_num','班级': 'grad_class_num','年级': 'enroll_year','专业':'grad_major' })

# 对uid进行哈希脱敏
dim_student = mask_student_id(temp_dim_student)


# 测试、验证
print(dim_student.columns)      # 只看列名
print(dim_student.sample(5))    # 随机抽取5行

print("=" * 40)
print("✅ dim_student 表已完成")
print("=" * 40)

    # 4.2 fact_major_reassign 表
# uid                          ← 来自 raw_graduation.csv  表的 "学号" 字段，经过哈希脱敏
# first_choice                 ← 来自 stage_reassign.csv  表的 “拟分流专业第一志愿” 字段 
# second_choice                ← 来自 stage_reassign.csv  表的 “拟分流专业第二志愿” 字段
# final_assigned_major         ← 来自 raw_graduation.csv  表的 “专业” 字段
# is_reassign                  ← 新建列，需要经过布尔运算：由stage_reassign.csv表的“拟分流专业第一志愿”和raw_graduation.csv  表的 “专业” 字段 进行比较，得出“yes”、“no”、“空值” 三种结果。（允许空值，因为2014级同学没有经过专业分流）

stage_fact_major_reassign = df_stg_reassign_ready[['学号','拟分流专业第一志愿','拟分流专业第二志愿','最终专业','is_reassign']]

temp_fact_major_reassign = stage_fact_major_reassign.rename(columns={'学号': 'uid','拟分流专业第一志愿': 'first_choice','拟分流专业第二志愿': 'second_choice','最终专业': 'final_assigned_major' })

fact_major_reassign = mask_student_id(temp_fact_major_reassign)

print(fact_major_reassign.columns)      # 只看列名
print(fact_major_reassign.sample(5))    # 随机抽取5行

print("=" * 40)
print("✅ fact_major_reassign 表已完成")
print("=" * 40)

    # 4.3 fact_gpa_records 表
# uid                          ← 来自 raw_graduation.csv  表的 "学号" 字段，经过哈希脱敏   
# academic_period              ← 新建列 (eg. ’第一学年‘, ’第二至四学年‘)
# gpa_score                    ← 来自 raw_last3y_gpa.csv  表的 “平均学分绩点” 字段+ stage_reassign.csv 表的“分流前_平均学分绩点” 字段 + raw_2014_first_year_GPA.csv 表的“平均学分绩点”字段

# 统一（大一学年的）平均学分绩点 列的列名
df_stg_reassign_ready = df_stg_reassign_ready.rename(columns={'分流前_平均学分绩点': '平均学分绩点'})

# 从df里选出特定的列
temp_2014_y1_gpa = df_2014_1y_gpa_ready[['学号','平均学分绩点']]
temp_201520162017_y1_gpa = df_stg_reassign_ready[['学号','平均学分绩点']]
temp_y234_gpa = df_raw_last3y_gpa_ready[['学号','平均学分绩点']]

# 纵向拼接两个临时表, 得到‘学号’列和‘平均学分绩点’列
temp_y1_gpa = pd.concat([temp_2014_y1_gpa , temp_201520162017_y1_gpa], ignore_index=True)

# 新建一列，全部填充“第一学年”/ "第二至四学年"
y1_gpa_ready = temp_y1_gpa.assign(academic_period = '第一学年')
y234_gpa_ready = temp_y234_gpa.assign(academic_period = '第二至四学年')

stage_fact_gpa_records = pd.concat([y1_gpa_ready,y234_gpa_ready], ignore_index=True)

# 调整列名
temp_fact_gpa_records = stage_fact_gpa_records.rename(columns={'平均学分绩点': 'gpa_score','学号':'uid'})

fact_gpa_records = mask_student_id(temp_fact_gpa_records)

# 构建 dim_student 表格时 被inner join排除的学生对应的GPA数据也应被排除在外
fact_gpa_records = fact_gpa_records[
    fact_gpa_records['uid'].isin(dim_student['uid'])
].reset_index(drop=True)

print(fact_gpa_records.columns)      # 只看列名
print(fact_gpa_records.sample(10))    # 随机抽取10行

print("=" * 40)
print("✅ fact_gpa_records 表已完成")
print("=" * 40)

# 验证表格重新组装是否出现错误
print(f"dim_student 行数：{len(dim_student)}")
print(f"fact_major_reassign 行数：{len(fact_major_reassign)}")
print(f"fact_gpa_records 行数：{len(fact_gpa_records)}")

# 验证 fact_gpa_records 的行数是否合理
print(f"  其中大一学年：{len(fact_gpa_records[fact_gpa_records['academic_period'] == '第一学年'])}")
print(f"  其中大二至四学年：{len(fact_gpa_records[fact_gpa_records['academic_period'] == '第二至四学年'])}")
# endregion


# region 5. 把三个数据表导入数据库

from sqlalchemy import create_engine

engine = create_engine('sqlite:////Users/juri/Downloads/教务系统导出和raw文件的加工步骤/art_school_reassign.db')

dim_student.to_sql('dim_student', con=engine, if_exists='replace', index=False)
fact_major_reassign.to_sql('fact_major_reassign', con=engine, if_exists='replace', index=False)
fact_gpa_records.to_sql('fact_gpa_records', con=engine, if_exists='replace', index=False)


# 验证数据是否成功写入
conn = sqlite3.connect('/Users/juri/Downloads/教务系统导出和raw文件的加工步骤/art_school_reassign.db')
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM dim_student")
print(f"dim_student 行数：{cursor.fetchone()[0]}")

cursor.execute("SELECT COUNT(*) FROM fact_major_reassign")
print(f"fact_major_reassign 行数：{cursor.fetchone()[0]}")

cursor.execute("SELECT COUNT(*) FROM fact_gpa_records")
print(f"fact_gpa_records 行数：{cursor.fetchone()[0]}")

conn.close()

print("=" * 40)
print("撰写数据字典ing, 各种检查df的细节")
print("=" * 40)

print("dim_student")
dim_student.info()

print("fact_gpa_records")
fact_gpa_records.info()

print("fact_major_reassign")
fact_major_reassign.info()
# endregion