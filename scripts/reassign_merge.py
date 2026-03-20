import pandas as pd

df_2015 = pd.read_csv("/Users/juri/Happy_coding/art_school_with_low_graduation_rate/data/raw/raw_2015_reassign.csv", encoding="utf-8-sig")
df_2016 = pd.read_csv("/Users/juri/Happy_coding/art_school_with_low_graduation_rate/data/raw/raw_2016_reassign.csv", encoding="utf-8-sig")
df_2017 = pd.read_csv("/Users/juri/Happy_coding/art_school_with_low_graduation_rate/data/raw/raw_2017_reassign.csv", encoding="utf-8-sig")

# 1. 处理2015年的“绩点合计”列
df_2015["绩点合计_归一"] = df_2015["绩点合计"] / 2

# 2. 删除2015年的 “平均学分绩点” 列和 “高考对应绩点” 列、把 "绩点合计_归一" 改成 “分流前_平均学分绩点” ；
#    把2016、2017年的 “平均学分绩点” 改成 “分流前_平均学分绩点” 。
df_2015 = df_2015.drop(columns=["平均学分绩点", "高考对应绩点","绩点合计"])
df_2015 = df_2015.rename(columns={"绩点合计_归一": "分流前_平均学分绩点"})

df_2016 = df_2016.rename(columns={"平均学分绩点":"分流前_平均学分绩点"} )
df_2017 = df_2017.rename(columns={"平均学分绩点":"分流前_平均学分绩点"} )

# 3. 合并三个分流志愿数据表并清洗字符前后的空格
merge_df = pd.concat( [df_2015, df_2016, df_2017], ignore_index=True)

merge_df = merge_df.apply(
    lambda col: col.str.strip().str.replace('\u3000', '', regex=False) 
    if col.dtype == 'object' else col
)

# 4. 标准化表格里的专业名称
merge_df = merge_df.replace({
    "视传":"视觉传达设计",
    "视觉传达":"视觉传达设计",
    "平面":"视觉传达设计",
    "服装":"服装与服饰设计",
    "服装设计":"服装与服饰设计",
    "环艺":"环境设计",
    "环境艺术":"环境设计",
    "环境艺术设计":"环境设计"
}
)

# 5. 取学号前四位数字，作为新增的“年级”列内容
merge_df['年级'] = merge_df['学号'].astype(str).str[:4]

# 6. 检验合并结果
# 6.1 检验行数
expected=len(df_2015)+len(df_2016)+len(df_2017)
actual = len(merge_df)
row_ok = expected == actual
print(f"\n【1. 行数验证】")

print(f"  预期总行数：{expected}，实际：{actual}")
print(f"  结果：{'✅ 通过' if row_ok else '❌ 有问题'}")

# 6.2 列名一致
col_expected = {"年级","学号","姓名","所在专业","所在班级","分流前_平均学分绩点","拟分流专业第一志愿","拟分流专业第二志愿","拟分流专业第三志愿","最终专业"}
col_actual = set(merge_df.columns)
col_ok = col_expected == col_actual
print(f"\n【2. 列名验证】")

print(f"  结果：{'✅ 通过' if col_ok else '❌ 列名不一致'}")
if not col_ok:
    diff_cols = col_actual.symmetric_difference(col_expected)
    if diff_cols:
        print(f" 合并后表格与预期表格的差异列：{diff_cols}")

# 6.3 检验空置 (合并前表格存在空值)
null_counts_expected = (df_2015.isnull().sum()+df_2016.isnull().sum()+df_2017.isnull().sum()).sum()
null_counts_actual = (merge_df.isnull().sum()).sum()
null_ok = (null_counts_expected == null_counts_actual)
print(f"\n【3. 空值验证】")

print(f"  预期空值数：{null_counts_expected}，实际：{null_counts_actual}")
print(f"  结果：{'✅ 通过' if null_ok else '❌ 有问题'}")

# 6.4 检验专业名称的表述是否归一
major_expected = {"视觉传达设计","环境设计","服装与服饰设计"}
major_actual_01 = set(merge_df["拟分流专业第一志愿"].dropna().unique()) 
major_actual_02 = set(merge_df["拟分流专业第二志愿"].dropna().unique()) 
major_actual_03 = set(merge_df["拟分流专业第三志愿"].dropna().unique()) 
major_ok = major_expected == major_actual_01 == major_actual_02 == major_actual_03
print(f"\n【4. 专业名称是否归一】")
print(f"  结果：{'✅ 通过' if major_ok else '❌ 专业名称仍需检查'}")
if not major_ok: 
    diff_major = (major_actual_01 - major_expected) | (major_actual_02 - major_expected) | (major_actual_03 - major_expected)
    if diff_major:
        print(f" 仍存在未归一的专业名称表述：{diff_major}")


# 7. 导出新的合并表格
merge_df.to_csv("/Users/juri/Downloads/教务系统导出和raw文件的加工步骤/stage_reassign.csv", index=False, encoding="utf-8-sig")

