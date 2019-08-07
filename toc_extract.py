import jiagu

jiagu.load_model('./model/cnc.model')  # 使用国家语委分词标准


def read_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        all_data = [line.strip('\n') for line in f.readlines()]
    result = []
    for data in all_data:
        # print(jiagu.seg(''.join(data)))
        one = []
        for ner in jiagu.ner(data):
            if ner is not 'O':
                one.append(ner)
        if one:
            result.append(one)

    text = '''
4. 香农的信息定义
假定事物状态可以用一个以经典集合论为基础的概率模型来描述，则信息就是用来消除不确定性的东西，或信息是事物运动状态或存在方式的不确定性描述。
但在实际中要寻找一个合适的概率模型往往是非常困难的，有时是否存在这样一种模型还值得探讨。此外，信息有很强的主观性和实用性，但该定义没有考虑信息接收者的主观特性和主观意义，不顾信息的具体含义、具体用途、重要程度和可能引起的后果等因素，这就与实际情况不完全一致。
'''
    keywords = jiagu.knowledge(text)  # 关键词
    print(keywords)
    # text = '姚明（Yao Ming），1980年9月12日出生于上海市徐汇区，祖籍江苏省苏州市吴江区震泽镇，前中国职业篮球运动员，司职中锋，现任中职联公司董事长兼总经理。'
    # knowledge = jiagu.knowledge(text)
    # print(knowledge)
    # print(result)


if __name__ == '__main__':
    path = r'./data_file/part_0.txt'
    read_txt(path)
