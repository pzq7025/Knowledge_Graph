import re
import jieba
import pynlpir

jieba.load_userdict('./source/entity.txt')


# pku的模型略好
# jiagu.load_model('./model/pku.model')  # 使用国家语委分词标准
class Toc:
    path = r'./data_file/part_0.txt'
    # 获取停用词的路径
    stop = r'./source/stop_word.txt'
    # 停用词表
    stop_list = []

    def get_stop_word(self):
        with open(self.stop, 'r', encoding='utf-8') as f:
            self.stop_list = [line.strip('\n') for line in f.readlines()]

    @staticmethod
    def part_re():
        """
        添加分层次结构的正则表达
        :return:
        """
        part_re_d = re.compile(r"\d\.\d", re.S)
        return part_re_d

    def get_struction(self):
        """
        对文本信息进行一个归类的处理  分出层次结构
        :param:
        :return:
        """
        with open(self.path, 'r', encoding='utf-8') as f:
            all_data = [line.strip('\n').replace(" ", '').replace(' ', '').replace("·", "_").replace('与', '-').replace('、', '-') for line in f.readlines()]
        parts = self.part_re()  # 获取正则匹配的表达式
        flag = re.findall(parts, all_data[1])  # 设定初始游标判断是否进行下一个的输入
        result = []  # 存贮总的信息
        f = []  # 存储当前单元的信息  如 ['1.1信息', '1.1.1信息的定义', '1.1.2信息的种类', '1.1.3信息的度量']
        for data in all_data:
            part_result = re.findall(parts, data)  # 对当前的阶段进行一个判断
            if len(part_result) > 1:  # 存在多个匹配值的时候取第一个匹配值
                part_result = [part_result[0]]
            if part_result == flag:
                if part_result:
                    # 如果在就进行归类
                    f.append(data)
                    continue
            else:
                # 如果不在就交换flag 并且将存储当前单元的数据置空
                flag = part_result
                if f:
                    result.append(f)
                f = [data, ]
        # for i in result:
        #     print(i)
        return result

    def toc_extract(self):
        """
        目录实体的抽取
        """
        results = self.get_struction()
        after = []
        global detail
        for one in results:
            if results.index(one) == 0:
                detail = self.title_detail(one)
            else:
                detail = self.content_detail(one)
            after.append(detail)
        # print(after)

    def title_detail(self, sentence):
        # ======================================================================================= 分开写为后面的段落结构划分
        """
        主标题的抽取
        :param sentence:
        :return:
        """
        result = []
        for word in sentence:
            mid = []
            segment = pynlpir.segment(word)
            # print(segment)
            # segment = jieba.lcut(word)
            for one in segment:
                # print(one)
                if one[0] not in self.stop_list:
                    mid.append(one[0])
            result.append(' '.join(mid))
        return result

    def content_detail(self, sentence):
        """
        子标题的抽取
        :param sentence:
        :return:
        """
        result = []
        for word in sentence:
            mid = []
            word = re.sub(r'\d', '', word)
            word = re.sub(r'\.', '', word)
            # segment = jieba.lcut(word)
            segment = pynlpir.segment(word)  # pos_names='all'
            print(segment)
            one = self.spo(segment)
            # result.append(' '.join(one))


            # for one in segment:
            #     if one not in self.stop_list:
            #         mid.append(one)
            # result.append(' '.join(mid))
        return result

    def spo(self, segment):
        """
        :param segment: 传入分词的列表
        :return:
        """
        mid = []
        stop_word = []
        for one in segment:
            if one[0] not in self.stop_list:
                stop_word.append(one)
        print(stop_word)
        return mid

    def start(self):
        try:
            pynlpir.open()
            pynlpir.nlpir.ImportUserDict(b'./source/entity.txt')  # 导入词典需要用到b转换成字节
            # pynlpir.nlpir.AddUserWord(u"泛在网络")
            self.get_stop_word()
            self.toc_extract()
        finally:
            pynlpir.close()


if __name__ == '__main__':
    toc = Toc()
    toc.start()
