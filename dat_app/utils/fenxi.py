import pymysql
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
from scipy.stats import rankdata

# 解决中文显示问题
plt.rcParams['font.sans-serif'] = ['KaiTi']  # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题



# 连接数据库
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


# 对dat_score进行简单数据分析并生成直方图
def show_sc():
    scores = fetch_dat_scores()

    if scores is not None:
        # 计算最小值、最大值、平均值、中位数等统计量（这里仅作为示例）
        min_score = min(scores)
        max_score = max(scores)
        avg_score = sum(scores) / len(scores)
        median_score = sorted(scores)[len(scores) // 2]

        print(f"最小分值: {min_score}")
        print(f"最大分值: {max_score}")
        print(f"平均分值: {avg_score}")
        print(f"中位数分值: {median_score}")
        print(f"极差：{np.ptp(scores)}")
        print(f"方差：{np.var(scores)}")
        print(f"标准差：{np.std(scores)}")
        print(f"变异系数：{np.mean(scores)}")

    else:
        print("没有可用的数据进行分析")


# 执行SQL并获取dat_score列数据并转换为DataFrame
def fetch_dat_scores_df():
    conn = connect_to_db()
    if conn is not None:
        try:
            cursor = conn.cursor()
            query = "SELECT dat_score FROM dat_app_dat_test"
            scores = execute_sql(cursor, query)

            # 将查询结果转换为pandas DataFrame
            df_scores = pd.DataFrame(scores, columns=['dat_score'])

            cursor.close()
            conn.close()

            return df_scores
        except Exception as e:
            print(f'获取数据时发生错误: {e}')
            return None
    else:
        print('未能成功连接数据库')
        return None


def ecdf(data):
    # 对数据排序
    sorted_data = np.sort(data)

    # 计算累积分布
    empirical_cdf = (np.arange(len(sorted_data)) + 1) / len(sorted_data)

    return sorted_data, empirical_cdf
# 对dat_score进行简单数据分析并生成直方图和箱型图
def analyze_and_plot_dat_scores():
    df_scores = fetch_dat_scores_df()

    if df_scores is not None and not df_scores.empty:
        # 直方图
        plt.figure(figsize=(10, 6))
        plt.hist(df_scores['dat_score'], bins='auto', edgecolor='black', alpha=0.7)
        plt.title('dat_score分布直方图')
        plt.xlabel('分值')
        plt.ylabel('频数')
        plt.grid(True)
        plt.show()
        # 箱型图
        plt.figure(figsize=(10, 6))
        plt.boxplot(df_scores['dat_score'], vert=True, patch_artist=True)
        plt.title('dat_score箱型图')
        plt.ylabel('分值')
        plt.grid(True)
        plt.show()
        #概率密度图
        sns.kdeplot(df_scores['dat_score'])
        plt.title('dat_score的概率密度分布')
        plt.xlabel('分值')
        plt.ylabel('密度')
        plt.show()

        #累积分布函数图
        # 假设df_scores是一个包含'dat_score'列的DataFrame
        scores = df_scores['dat_score'].values
        x, y = ecdf(scores)

        # 使用matplotlib绘制ECDF
        plt.plot(x, y, marker='.', linestyle='none')
        plt.xlabel('分数')
        plt.ylabel('累积概率')
        plt.margins(0.02)  # Smaller margins
        plt.grid(True)

        plt.show()

    else:
        print("没有可用的数据进行分析")


# 调用函数进行分析并显示图表
if __name__ == '__main__':
    show_sc()
    analyze_and_plot_dat_scores()
