from py2neo import Node, Graph, Relationship

graph = Graph("http://10.120.33.198:7474/browser/", username="neo4j", password='123123')


class BookGraph:
    cursor = graph.begin()

    @staticmethod
    def get_master():
        x = graph.nodes.match('master', name='ACM').first()
        return x

    """
    一般和参考
    硬件
    计算机系统组织
    网络
    软件及其工程
    计算理论
    计算数学
    信息系统
    安全和隐私
    以人为本的计算
    计算方法
    应用计算
    社交和专业话题
    """

    def find(self):
        master = self.get_master()
        node_list = [
            'General and reference',
            'Hardware',
            'Computer systems organization',
            'Networks',
            'Software and its engineering',
            'Theory of computation',
            'Mathematics of computing',
            'Information systems',
            'Security and privacy',
            'Human - centered computing',
            'Computing methodologies',
            'Applied computing',
            'Social and professional topics',
        ]

        for i in node_list:
            node = Node("first", name=i)
            self.cursor.create(node)
            r = Relationship(master, 'branch', node)
            self.cursor.create(r)
        self.cursor.commit()
        print("Successfully!")

    def add_one(self):
        pass

    def add_batch(self):
        pass

    def create_toc_node(self):
        toc_list = []
        for i in toc_list:
            node = Node("Toc", name=i, book='IC')
            self.cursor.create(node)
            # r = Relationship(master, 'branch', node)
            # self.cursor.create(r)
        self.cursor.commit()
        print("Successfully!")


if __name__ == '__main__':
    book_graph = BookGraph()
    book_graph.find()
