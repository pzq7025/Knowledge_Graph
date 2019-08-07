import re
import jieba
import jieba.posseg as pseg

jieba.load_userdict('./source/entity.txt')


# pku的模型略好
# jiagu.load_model('./model/pku.model')  # 使用国家语委分词标准
class Toc:
    index = 0
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
        path = r'./data_file/part_' + str(self.index) + '.txt'
        with open(path, 'r', encoding='utf-8') as f:
            all_data = [line.strip('\n').replace(" ", '').replace(' ', '').replace("·", "_").replace('-', '').replace('*', '').replace('与', '-').replace('、', '-').replace('和', '-').replace('从', '&').replace('看', '&') for line in f.readlines()]
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
            if detail:
                after.append(detail)
        # for i in after:
        #     print(i)

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
            segment = jieba.lcut(word)
            for one in segment:
                # print(one)
                if one not in self.stop_list:
                    mid.append(one)
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
            word = re.sub(r'\d', '', word)
            word = re.sub(r'\.', '', word)
            segment = pseg.lcut(word)
            # print(segment)
            one = self.spo(segment)
            if one:
                result.append(one)
        # print(result)
        return result

    def spo(self, segment):
        """
        :param segment: 传入分词的列表
        :return:
        """
        # print(segment)
        convert = []  # 存储转换后pair
        for word, tags in segment:  # 转换pair
            # for i in one:
            #     t.append(i)
            convert.append((word, tags))

        stop_after = []  # 存储去除停用词的数组
        for i in convert:  # 去重停用词
            if i[0] not in self.stop_list:
                if i:
                    stop_after.append(i)

        print(stop_after)
        entity_chunk = ['t', 'v', 'n', 'vn']  # 向前的词
        after = ['n', 'v', 'l']  # 最后的词
        """
        从······看  替换成了-    -
        与 、 和 替换成了 -
        """
        mid = []  # 返回的spo三元组
        for one in range(len(stop_after) - 1, -1, -1):
            if len(stop_after) == 2:
                if stop_after[one][1] in after and stop_after[one - 1][1] in entity_chunk:
                    combine = stop_after[one - 1][0] + stop_after[one][0]
                    mid.append(combine)
                    break
                else:
                    mid.append(stop_after[one])
            if len(stop_after) == 3:
                pass

            # if stop_after[one][1] in after and after[one - 1][1] in entity_chunk:
            #     combine = after[one - 1][0] + after[one][0]
            #     mid.append(combine)
            #     break
        # if one[i][1] in after and one[i - 1][1] in entity_chunk:
        #     combine = one[i - 1][0] + one[i][0]
        #     mid.append(combine)
        #     break
        # for i in stop_after:
        #     # print(i)
        #     if len(stop_after) == 1:
        #         mid.append(i[0])
        #         break
        #     if len(stop_after) == 2:
        #         mid.append((stop_after[0][0]+stop_after[1][0]))
        #         break
        #     if len(stop_after) == 3:
        #         # if i[1] in after:
        #         #     if stop_after[stop_after.index(i) - 1][1] in entity_chunk:
        #         #         print(stop_after[stop_after.index(i) + 1])
        #         #         store = stop_after[stop_after.index(i) + 1][0] + i[0]
        #         store = stop_after[1][0] + stop_after[2][0]
        #         mid.append((stop_after[0][0], ' ', store))
        #         break
        #     if len(stop_after) > 4:
        #         mid.append(stop_after)
        #         break
        #     if len(stop_after) == 4:
        #         break
        #     if i[0] == '-':
        #         mid.append(stop_after)
        #         break
        print(f"我是mid：{mid}")
        return mid

    def start(self):
        # for i in range(7):
        self.get_stop_word()
        self.toc_extract()
        self.index += 1


if __name__ == '__main__':
    toc = Toc()
    toc.start()
