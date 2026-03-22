# 艺术学院数据分析：服装设计专业毕业率归因模型
(Art School Data Analysis: Attribution Model for Declining Graduation Rates)

## 1. 业务背景与任务 (Business Context & Task)
* **业务痛点：** 服装设计专业毕业率连续三年低于预期，当前已跌至71%，逼近停招红线（70%）。本项目旨在通过归因分析定位核心流失环节，输出挽救该专业招生资质的干预策略。
* **核心任务：** 输出结构化洞察，为教务干预提供数据支撑。
* **项目性质：** 项目重构，具体请参考  **7.历史版本记录  (Version History)**

## 2. 核心洞察与商业价值 (Executive Summary)
* **洞察：** [列出最重要的 1-2 个基于多维漏斗过滤出的结论，必须包含具体数据]
* **建议与价值：** [提出 1 个直接指向业务闭环的 Action，并标明预估的商业增量（如 ARR）]

## 3. 数据集声明 (Data Origin)
* **数据来源：** 某学校教务处网站
* **时间跨度：** 2014-2017级学生的在校时间
* **数据体量：** ETL 阶段后的数据库文件 233kb，涉及约 300 位设计系学生
* **隐私处理：** 数据库中的学生学号已经过 SHA-256 哈希脱敏处理，姓名字段已在 ETL 阶段删除。

## 4. 工程架构 (Repository Structure)
```
project_folder/
├── data/                         # 原始数据与中间表 (已加入 .gitignore)
│   ├── raw/                      # 原始数据 (CSV 数据集)
│   └── processed/ 
├── docs/                         # 数据字典与日志
│   ├── analysis_log.md           
│   └── data_dictionary.md
├── notebooks/                    # 用于探索性数据分析 (EDA) 的 Jupyter/R Markdown 文件
├── scripts/                      # 数据处理与分析脚本 (SQL/R/Python)
├── visuals/                      # 核心可视化输出
├── requirements.txt              # Python 依赖清单
└── README.md                     # 项目说明书
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