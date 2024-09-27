from gensim.models import KeyedVectors
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity, paired_distances, euclidean_distances
import matplotlib.colors as colors
import matplotlib.pyplot as plt
import matplotlib
from datetime import datetime
from dat_app import models
from matplotlib import rcParams
import os

# 假设SIMHEI.TTF就在你的脚本所在目录
font_path = './SIMHEI.TTF'

# 确保文件存在
if not os.path.exists(font_path):
    print("警告：找不到字体文件SIMHEI.TTF，请检查路径是否正确。")
else:
    # 配置matplotlib使用此字体
    rcParams['font.family'] = 'sans-serif'
    rcParams['font.sans-serif'] = ['SimHei']  # 使用字体的英文名称或确保与实际字体文件内部名称匹配

    # 对于中文支持的额外配置
    rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
matplotlib.use('Agg')
general_model = None


def load_word2vec_model():
    global general_model
    if general_model is None:
        # general_model = KeyedVectors.load('./dat_app/utils/models/w2v.wv')
        general_model = KeyedVectors.load('./models/w2v.wv')


# 计算两个词的相关程度分数
def two_words(word1, word2):
    if general_model is None:
        # 加载通用模型
        load_word2vec_model()
    x = np.array([general_model[word1]])
    y = np.array([general_model[word2]])
    # 余弦距离
    dis = paired_distances(x, y, metric="cosine")
    # 得分
    score = int(dis * 100)
    return score


# 计算得分的图片
def picture_dat(valid_words, username, dat_score):
    # 中文显示
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

    # 词数
    min_value = len(valid_words)

    # 判断词数
    if min_value < 5:
        return "/static/img/tips.jpg"
    if min_value > 5:
        n = min_value

        if n == 6:
            array_list = [
                [0, 0, 0, 0, 0, 0],
                [two_words(valid_words[1], valid_words[0]), 0, 0, 0, 0, 0],
                [two_words(valid_words[2], valid_words[0]), two_words(valid_words[2], valid_words[1]), 0, 0, 0, 0],
                [two_words(valid_words[3], valid_words[0]), two_words(valid_words[3], valid_words[1]),
                 two_words(valid_words[3], valid_words[2]), 0, 0, 0],
                [two_words(valid_words[4], valid_words[0]), two_words(valid_words[4], valid_words[1]),
                 two_words(valid_words[4], valid_words[2]), two_words(valid_words[4], valid_words[3]), 0, 0],
                [two_words(valid_words[5], valid_words[0]), two_words(valid_words[5], valid_words[1]),
                 two_words(valid_words[5], valid_words[2]), two_words(valid_words[5], valid_words[3]),
                 two_words(valid_words[5], valid_words[4]), 0]
            ]
        elif n == 7:
            array_list = [
                [0, 0, 0, 0, 0, 0, 0],
                [two_words(valid_words[1], valid_words[0]), 0, 0, 0, 0, 0, 0],
                [two_words(valid_words[2], valid_words[0]), two_words(valid_words[2], valid_words[1]), 0, 0, 0, 0, 0],
                [two_words(valid_words[3], valid_words[0]), two_words(valid_words[3], valid_words[1]),
                 two_words(valid_words[3], valid_words[2]), 0, 0, 0, 0],
                [two_words(valid_words[4], valid_words[0]), two_words(valid_words[4], valid_words[1]),
                 two_words(valid_words[4], valid_words[2]), two_words(valid_words[4], valid_words[3]), 0, 0, 0],
                [two_words(valid_words[5], valid_words[0]), two_words(valid_words[5], valid_words[1]),
                 two_words(valid_words[5], valid_words[2]), two_words(valid_words[5], valid_words[3]),
                 two_words(valid_words[5], valid_words[4]), 0, 0],
                [two_words(valid_words[6], valid_words[0]), two_words(valid_words[6], valid_words[1]),
                 two_words(valid_words[6], valid_words[2]),
                 two_words(valid_words[6], valid_words[3]), two_words(valid_words[6], valid_words[4]),
                 two_words(valid_words[6], valid_words[5]), 0]
            ]
        elif n == 8:
            array_list = [
                [0, 0, 0, 0, 0, 0, 0, 0],
                [two_words(valid_words[1], valid_words[0]), 0, 0, 0, 0, 0, 0, 0],
                [two_words(valid_words[2], valid_words[0]), two_words(valid_words[2], valid_words[1]), 0, 0, 0, 0, 0,
                 0],
                [two_words(valid_words[3], valid_words[0]), two_words(valid_words[3], valid_words[1]),
                 two_words(valid_words[3], valid_words[2]), 0, 0, 0, 0, 0],
                [two_words(valid_words[4], valid_words[0]), two_words(valid_words[4], valid_words[1]),
                 two_words(valid_words[4], valid_words[2]), two_words(valid_words[4], valid_words[3]), 0, 0, 0, 0],
                [two_words(valid_words[5], valid_words[0]), two_words(valid_words[5], valid_words[1]),
                 two_words(valid_words[5], valid_words[2]), two_words(valid_words[5], valid_words[3]),
                 two_words(valid_words[5], valid_words[4]), 0, 0, 0],
                [two_words(valid_words[6], valid_words[0]), two_words(valid_words[6], valid_words[1]),
                 two_words(valid_words[6], valid_words[2]),
                 two_words(valid_words[6], valid_words[3]), two_words(valid_words[6], valid_words[4]),
                 two_words(valid_words[6], valid_words[5]), 0, 0],
                [two_words(valid_words[7], valid_words[0]), two_words(valid_words[7], valid_words[1]),
                 two_words(valid_words[7], valid_words[2]),
                 two_words(valid_words[7], valid_words[3]), two_words(valid_words[7], valid_words[4]),
                 two_words(valid_words[7], valid_words[5]), two_words(valid_words[7], valid_words[6]), 0]
            ]
        elif n == 9:
            array_list = [
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [two_words(valid_words[1], valid_words[0]), 0, 0, 0, 0, 0, 0, 0, 0],
                [two_words(valid_words[2], valid_words[0]), two_words(valid_words[2], valid_words[1]), 0, 0, 0, 0, 0, 0,
                 0],
                [two_words(valid_words[3], valid_words[0]), two_words(valid_words[3], valid_words[1]),
                 two_words(valid_words[3], valid_words[2]), 0, 0, 0, 0, 0, 0],
                [two_words(valid_words[4], valid_words[0]), two_words(valid_words[4], valid_words[1]),
                 two_words(valid_words[4], valid_words[2]), two_words(valid_words[4], valid_words[3]), 0, 0, 0, 0, 0],
                [two_words(valid_words[5], valid_words[0]), two_words(valid_words[5], valid_words[1]),
                 two_words(valid_words[5], valid_words[2]), two_words(valid_words[5], valid_words[3]),
                 two_words(valid_words[5], valid_words[4]), 0, 0, 0, 0],
                [two_words(valid_words[6], valid_words[0]), two_words(valid_words[6], valid_words[1]),
                 two_words(valid_words[6], valid_words[2]),
                 two_words(valid_words[6], valid_words[3]), two_words(valid_words[6], valid_words[4]),
                 two_words(valid_words[6], valid_words[5]), 0, 0, 0],
                [two_words(valid_words[7], valid_words[0]), two_words(valid_words[7], valid_words[1]),
                 two_words(valid_words[7], valid_words[2]),
                 two_words(valid_words[7], valid_words[3]), two_words(valid_words[7], valid_words[4]),
                 two_words(valid_words[7], valid_words[5]), two_words(valid_words[7], valid_words[6]), 0, 0],
                [two_words(valid_words[8], valid_words[0]), two_words(valid_words[8], valid_words[1]),
                 two_words(valid_words[8], valid_words[2]),
                 two_words(valid_words[8], valid_words[3]), two_words(valid_words[8], valid_words[4]),
                 two_words(valid_words[8], valid_words[5]), two_words(valid_words[8], valid_words[6]),
                 two_words(valid_words[8], valid_words[7]), 0]
            ]
        elif n == 10:
            array_list = [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [two_words(valid_words[1], valid_words[0]), 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [two_words(valid_words[2], valid_words[0]), two_words(valid_words[2], valid_words[1]), 0, 0, 0, 0, 0, 0,
                 0, 0],
                [two_words(valid_words[3], valid_words[0]), two_words(valid_words[3], valid_words[1]),
                 two_words(valid_words[3], valid_words[2]), 0, 0, 0, 0, 0, 0, 0],
                [two_words(valid_words[4], valid_words[0]), two_words(valid_words[4], valid_words[1]),
                 two_words(valid_words[4], valid_words[2]), two_words(valid_words[4], valid_words[3]), 0, 0, 0, 0, 0,
                 0],
                [two_words(valid_words[5], valid_words[0]), two_words(valid_words[5], valid_words[1]),
                 two_words(valid_words[5], valid_words[2]), two_words(valid_words[5], valid_words[3]),
                 two_words(valid_words[5], valid_words[4]), 0, 0, 0, 0, 0],
                [two_words(valid_words[6], valid_words[0]), two_words(valid_words[6], valid_words[1]),
                 two_words(valid_words[6], valid_words[2]),
                 two_words(valid_words[6], valid_words[3]), two_words(valid_words[6], valid_words[4]),
                 two_words(valid_words[6], valid_words[5]), 0, 0, 0, 0],
                [two_words(valid_words[7], valid_words[0]), two_words(valid_words[7], valid_words[1]),
                 two_words(valid_words[7], valid_words[2]),
                 two_words(valid_words[7], valid_words[3]), two_words(valid_words[7], valid_words[4]),
                 two_words(valid_words[7], valid_words[5]), two_words(valid_words[7], valid_words[6]), 0, 0, 0],
                [two_words(valid_words[8], valid_words[0]), two_words(valid_words[8], valid_words[1]),
                 two_words(valid_words[8], valid_words[2]),
                 two_words(valid_words[8], valid_words[3]), two_words(valid_words[8], valid_words[4]),
                 two_words(valid_words[8], valid_words[5]), two_words(valid_words[8], valid_words[6]),
                 two_words(valid_words[8], valid_words[7]), 0, 0],
                [two_words(valid_words[9], valid_words[0]), two_words(valid_words[9], valid_words[1]),
                 two_words(valid_words[9], valid_words[2]),
                 two_words(valid_words[9], valid_words[3]), two_words(valid_words[9], valid_words[4]),
                 two_words(valid_words[9], valid_words[5]), two_words(valid_words[9], valid_words[6]),
                 two_words(valid_words[9], valid_words[7]), two_words(valid_words[9], valid_words[8]), 0]
            ]
        harvest = np.array(array_list)
        # 绘图
        plt.figure(dpi=600)
        plt.xticks(range(min_value), labels=valid_words, rotation=60)
        plt.yticks(range(min_value), labels=valid_words)

        # 设置标题
        now = datetime.now()
        timestamp = now.timestamp()
        title = "thescoreis" + str(dat_score) + str(timestamp)
        # plt.title(title)

        for i in range(min_value):
            for j in range(min_value):
                text = plt.text(j, i, harvest[i, j], ha="center", va="center", color="w")

        # cmap = colors.ListedColormap(['white', 'lightblue', 'blue', 'darkblue', 'purple'])
        # cmap = colors.ListedColormap(['FloralWhite', 'LightSalmon ', 'Tomato', 'DarkOrange', 'GoldEnrod'])
        # cmap = colors.ListedColormap(['floralwhite', 'salmon', 'Tomato', 'DarkOrange', 'goldenrod'])
        cmap = colors.ListedColormap(['azure', 'paleturquoise', 'lightskyblue', 'cornflowerblue', 'royalblue'])
        plt.imshow(harvest, cmap=cmap)

        # filepath = "./dat_app/static/img/" + title + ".jpg"
        filepath = "../static/img/" + title + ".jpg"
        plt.savefig(filepath)
        pic_path = "/static/img/" + title + ".jpg"
        plt.close()
        return pic_path


# 计算得分
def count_dat(data_dict, username):
    # 加载并读取预训练模型
    if general_model is None:
        # 加载通用模型
        load_word2vec_model()

    words_list = []
    # 判断存在多少个有效词数
    for key, value in data_dict.items():
        words_list.append(value)

    # 有效词列表
    valid_words = []
    for word in words_list:
        if word in general_model:
            valid_words.append(word)

    # 得到最大有效词数
    effective_num = len(valid_words)

    # 计算分数
    dat_score = []
    for x in range(1, effective_num):
        for y in range(0, x):
            dat_score.append(two_words(valid_words[x], valid_words[y]))
    # print(dat_score)
    # 平均值，最终得分
    dat = int(np.mean(dat_score))
    filepath = picture_dat(valid_words, username, dat)

    # 超越多少人
    all_data = models.dat_test.objects.all()
    scores = all_data.values('dat_score')
    scores_list = []
    for score in scores:
        scores_list.append(score["dat_score"])
    smaller = []
    for score in scores_list:
        if score < dat:
            smaller.append(score)
    # 超越了多少人
    percentage = (len(smaller) / len(scores_list)) * 100

    # 返回一个结果给后端
    return_data = {"dat_score": dat,
                   "effective_num": effective_num, "filepath": filepath, "per": percentage}
    print(return_data)
    return return_data
