import thulac
import jieba
from snownlp import SnowNLP
import pynlpir

text_1 = "冯·诺伊曼体系结构"
# text_1 = "计算机网络的定义与分类"
# thu1 = thulac.thulac()  # 默认模式
# text = thu1.cut(text_1)  # 进行一句话分词
# print(f"我是thulac:{text}")
#
# print(f"我是jieba:{jieba.lcut(text_1)}")
#
# s = SnowNLP(text_1)
# print(f"我是snownlp:{s.words}")
#
# text__2 = '''
# 自然语言处理是计算机科学领域与人工智能领域中的一个重要方向。
# 它研究能实现人与计算机之间用自然语言进行有效通信的各种理论和方法。
# 自然语言处理是一门融语言学、计算机科学、数学于一体的科学。
# 因此，这一领域的研究将涉及自然语言，即人们日常使用的语言，
# 所以它与语言学的研究有着密切的联系，但又有重要的区别。
# 自然语言处理并不是一般地研究自然语言，
# 而在于研制能有效地实现自然语言通信的计算机系统，
# 特别是其中的软件系统。因而它是计算机科学的一部分。
# '''
#
# s = SnowNLP(text__2)
# print(f"我是snownlp text:{s.summary(3)}")

try:
    pynlpir.open()
    segments = pynlpir.segment(text_1, pos_names='all')
    # pynlpir.nlpir.AddUserWord()
    key_words = pynlpir.get_key_words(text_1, weighted=True)
    print(f"我是pynlpier的segment:{segments}")
    print(f"我是pynlpier的key_words:{key_words}")
finally:
    pynlpir.close()
