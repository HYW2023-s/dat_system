from gensim.models import KeyedVectors

# 请将腾讯AI实验室的word2vec与该文件放在同一目录下，输入文件名后，运行本程序
file = 'tencent-ailab-embedding-zh-d200-v0.2.0.txt'
model = KeyedVectors.load_word2vec_format(file, binary=False)

model.save('w2v.wv')
