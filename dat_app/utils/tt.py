from pyecharts import options as opts
from pyecharts.charts import Bar, Boxplot, Line
import pymysql
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns

# 解决中文显示问题
plt.rcParams['font.sans-serif'] = ['KaiTi']  # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

def connect_to_db():
    try:
        return pymysql.connect(
            host="8.134.140.51", user="yesong", port=20308, password="uPIFktq8NDi1kV6",
            database="ai_robot", charset="utf8mb4"
        )
    except pymysql.MySQLError as e:
        print(f'无法连接数据库: {e}')
        return None


# SQL执行
def execute_sql(cursor, query, params=None, fetchone=False):
    try:
        cursor.execute(query, params)
        return cursor.fetchone() if fetchone else cursor.fetchall()
    except pymysql.MySQLError as e:
        print(f'SQL 报错: {e}')
        return None


# 执行SQL并获取dat_score列数据
def fetch_dat_scores():
    conn = connect_to_db()
    if conn is not None:
        try:
            cursor = conn.cursor()
            query = "SELECT dat_score FROM dat_app_dat_test"
            scores = execute_sql(cursor, query)

            # 数据清洗与转换成数值列表
            scores_list = [score[0] for score in scores]

            cursor.close()
            conn.close()

            return scores_list
        except Exception as e:
            print(f'获取数据时发生错误: {e}')
            return None
    else:
        print('未能成功连接数据库')
        return None
scores = fetch_dat_scores()
df_scores = pd.DataFrame(scores, columns=['dat_score'])

# 直方图
bar = (
    Bar()
    .add_xaxis(df_scores.index.tolist())
    .add_yaxis("分值", df_scores['dat_score'].tolist(), category_gap="50%")
    .set_global_opts(title_opts=opts.TitleOpts(title="dat_score分布直方图"), xaxis_opts=opts.AxisOpts(name="分值"), yaxis_opts=opts.AxisOpts(name="频数"))
)

# 箱型图
boxplot = (
    Boxplot()
    .add_xaxis(["dat_score"])
    .add_yaxis("", [df_scores['dat_score'].describe().values.tolist()])
    .set_global_opts(title_opts=opts.TitleOpts(title="dat_score箱型图"), xaxis_opts=opts.AxisOpts(name=""), yaxis_opts=opts.AxisOpts(name="分值"))
)

# 概率密度图（使用 Line 图表代替）
scores = df_scores['dat_score'].values
density, bins = np.histogram(scores, bins=20, density=True)
line = (
    Line()
    .add_xaxis(bins.tolist())
    .add_yaxis("密度", density.tolist(), is_smooth=True, symbol="circle", symbol_size=6, label_opts=opts.LabelOpts(is_show=False))
    .set_global_opts(title_opts=opts.TitleOpts(title="dat_score的概率密度分布"), xaxis_opts=opts.AxisOpts(name="分值"), yaxis_opts=opts.AxisOpts(name="密度"))
)

# 累积分布函数图
x = np.sort(scores)
y = (np.arange(len(scores)) + 1) / len(scores)

line_cdf = (
    Line()
    .add_xaxis(x.tolist())
    .add_yaxis("累积概率", y.tolist(), is_smooth=True, label_opts=opts.LabelOpts(is_show=False))
    .set_global_opts(title_opts=opts.TitleOpts(title="dat_score的累积分布函数图"), xaxis_opts=opts.AxisOpts(name="分数"), yaxis_opts=opts.AxisOpts(name="累积概率"))
)

# 生成图表
bar.render_notebook()
boxplot.render_notebook()
line.render_notebook()
line_cdf.render_notebook()
