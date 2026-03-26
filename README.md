# 服装设计专业毕业率归因模型
基于 SQLite + Python 的教育数据分析项目，探查大类分流制度对服装专业毕业率的影响



## 1. 业务背景与任务 (Business Context & Task)
* **业务痛点：** 服装与服饰设计专业毕业率连续三年低于预期，2017 级毕业率已跌至 68%，学校就停止服装专业招收新生一事进行内部讨论。本项目旨在通过归因分析、定位核心流失环节，输出提振该专业学生毕业率的干预策略。
* **核心任务：** 输出结构化洞察，为教务干预提供数据支撑。
* **项目性质：** 真实落地项目。此次为项目重构，具体请参考   ## 7. 历史版本记录

## 2. 核心洞察与商业价值 (Executive Summary)
* **洞察一：** 88%的大类分流志愿集中在视传或环艺专业，服装专业成为调剂学生的主要去向。
* **洞察二：** [列出最重要的 1-2 个基于多维漏斗过滤出的结论，必须包含具体数据]
* **洞察三：** [列出最重要的 1-2 个基于多维漏斗过滤出的结论，必须包含具体数据]


## 3. 数据集声明 (Data Origin)
* **数据来源：** 某学校教务处网站
* **时间跨度：** 2014-2017级学生的在校时间
* **数据体量：** ETL 阶段后的数据库文件 233kb，涉及约 300 位设计系学生
* **隐私处理：** 数据库中的学生学号已经过 SHA-256 哈希脱敏处理，姓名字段已在 ETL 阶段删除。

## 4. 工程架构 (Repository Structure)
```
project_folder/
├── data/                                                 # 原始数据与中间表 (已加入 .gitignore)
│   ├── raw/                                              # 原始数据 (含学生个人信息，不上传)
│   ├── stage/                                            # 中间表 (含学生个人信息，不上传)
│   └── processed/                                        # 清洗后数据库
│       └── art_school_reassign.db                        # 学号已哈希脱敏
├── docs/                                                 # 数据字典        
│   └── data_dictionary.md
├── notebooks/                                            # 用于探索性数据分析 (EDA) 的 Jupyter/R Markdown 文件
├── scripts/                                              # 数据处理与分析脚本 (SQL/R/Python)
├── visuals/                                              # 核心可视化输出
├── requirements.txt                                      # Python 依赖清单
└── README.md                                             # 项目说明书
```

## 5. 环境与复现指南 (Reproduction Guide)
**工具栈：**  Python 3.13 / SQL
**核心库：**  Pandas (数据清洗), Matplotlib/Seaborn (可视化)

**复现步骤：**
1. 克隆本项目仓库：
   `git clone [你的仓库链接]`
2. 安装依赖环境：
   * Python 依赖包安装：在终端执行 `pip install -r requirements.txt`
   * R 依赖包安装：在 R 控制台执行 `install.packages(c("tidyverse", "geohashTools"))` [根据实际情况修改]
3. 执行数据清洗与分析：
   * 运行 `scripts/01_data_cleaning.sql` 生成底层宽表。
   * 运行 `scripts/02_eda_and_metrics.sql` 提取核心特征。

## 6. 核心分析输出 (Key Visualizations)
[此处仅插入 1-2 张数据墨水比最高、最能支撑 Executive Summary 的图表]
![图表说明](visuals/your_chart_name.png)

## 7. 历史版本记录  (Version History)
(对比 V1.0 (Excel) 与 V2.0 (Python/SQL) 在数据处理效率、自动化程度上的差异。)


### 📊 完整分析报告

详细的分析过程、图表和业务建议请参阅：
[服装设计专业毕业率归因模型 - Notion](https://www.notion.so/yuel/3207761aa52a80778bfbf14fbb50f8f6)