import cv2 as cv
import numpy as np
import time


class Node(object):
    def __init__(self, id, value):
        self.id = id
        # 表示这个顶点从0开始的编号，y*width+x
        self.value = value
        # 表示这个结点的RGB
        self.root = self.id
        # 表示这个顶点的根节点
        self.size = 1

        self.max_weight = 0


class Edge(object):
    def __init__(self, node1, node2, weight):
        self.node1 = node1
        self.node2 = node2
        self.weight = weight
        # 通过点点权创建一条边


class Graph(object):
    def __init__(self, image_path, neighborhood_8=True, min_size=200):
        self.image = cv.imread(image_path)
        self.image_height = int(self.image.shape[0])
        self.image_width = int(self.image.shape[1])
        self.merge_constant = (self.image_width * self.image_height) / 1e2  # 内部差的一个参数，就是第二个数上面的分子

        self.neighborhood_8 = neighborhood_8
        self.min_size = min_size

        self.nodes = self.create_nodes()
        self.edges = self.create_edges()

        self._label_image = None
        self._label_no = None
        self._segmented_image = None

    def create_nodes(self):
        nodes = []
        for y in range(self.image_height):
            for x in range(self.image_width):
                nodes.append(Node(y * self.image_width + x, self.image[y, x]))
        return nodes

    # weight 接下来求的是两条边的权值
    def diff(self, node1, node2):
        value1 = self.nodes[node1].value
        value2 = self.nodes[node2].value
        result = np.sqrt(np.sum((value1 - value2) ** 2))  # 因为他有rgb三个类型值，所以求的是开方平均值
        return result

    def create_edges(self):
        edges = []
        for y in range(self.image_height):
            for x in range(self.image_width):
                node1 = y * self.image_width + x
                if x > 0:
                    node2 = y * self.image_width + (x - 1)
                    weight = self.diff(node1, node2)
                    edges.append(Edge(node1, node2, weight))
                if y > 0:
                    node2 = (y - 1) * self.image_width + x
                    weight = self.diff(node1, node2)
                    edges.append(Edge(node1, node2, weight))
                if self.neighborhood_8:
                    if x > 0 and y > 0:
                        node2 = (y - 1) * self.image_width + (x - 1)
                        weight = self.diff(node1, node2)
                        edges.append(Edge(node1, node2, weight))
                    if x > 0 and y < self.image_height - 1:
                        node2 = (y + 1) * self.image_width + (x - 1)
                        weight = self.diff(node1, node2)
                        edges.append(Edge(node1, node2, weight))
        result = sorted(edges, key=lambda edge: edge.weight)
        return result

    # 内部差函数
    def threshold(self, root1, root2):
        threshold1 = self.nodes[root1].max_weight + self.merge_constant / self.nodes[root1].size
        threshold2 = self.nodes[root2].max_weight + self.merge_constant / self.nodes[root2].size
        result = max(threshold1, threshold2, 5)
        return result

    def find_root(self, node):
        root = node
        while root != self.nodes[root].root:
            root = self.nodes[root].root
        return root

    def segment_graph(self):
        for edge in self.edges:
            root1 = self.find_root(edge.node1)
            root2 = self.find_root(edge.node2)
            if root1 != root2:
                if edge.weight < self.threshold(root1, root2):  # 为什么是小于最大值，不是大于最小值
                    self.merge(root1, root2)
        return

    def merge_small_components(self):
        for edge in self.edges:
            root1 = self.find_root(edge.node1)
            root2 = self.find_root(edge.node2)
            if root1 != root2:
                if self.nodes[root1].size < self.min_size or self.nodes[root2].size < self.min_size:
                    self.merge(root1, root2)
        return

    def merge(self, root1, root2, weight=None):
        if root1 < root2:
            self.nodes[root2].root = root1
            self.nodes[root1].size = self.nodes[root1].size + self.nodes[root2].size
            if weight is not None and self.nodes[root1].max_weight < weight:
                self.nodes[root1].max_weight = weight

        if root1 > root2:
            self.nodes[root1].root = root2
            self.nodes[root2].size = self.nodes[root1].size + self.nodes[root2].size
            if weight is not None and self.nodes[root2].max_weight < weight:
                self.nodes[root2].max_weight = weight

    def generate_label_image(self):
        root_dict = dict()
        next_label = 0
        self.segment_graph()
        # self.merge_small_components()
        _label_image = np.zeros(shape=self.image.shape[:2], dtype=np.uint8)  # dtype=np.uint8的目的是输出图象
        for y in range(self.image_height):
            for x in range(self.image_width):
                index = y * self.image_width + x
                root = self.find_root(index)
                if root not in root_dict:
                    root_dict[root] = next_label
                    _label_image[y, x] = next_label
                    next_label += 1
                else:
                    the_label = root_dict[root]
                    _label_image[y, x] = the_label
        self._label_image = _label_image
        self._label_no = next_label
        return self._label_image, self._label_no

    def random_color(self,i):
        #color_table=[(0,0,0),(128,138,135),(252,230,202),(255, 0, 0), (255, 255, 0),(0, 255, 0), (0, 0, 255), (255, 215, 0), (138, 43, 226),(0, 155, 155),(155, 155, 0)]
        color_table=[(255,192,203),(128,0,128),(106,90,205),(0,0,255),(135,206,235),(0,128,0),(189,183,107),(255,215,0),(255,0,0),(0,0,0),
                    (123,104,238),(65,105,225),(0,100,0),(255,255,0),]
        result = color_table[i % 10]
        return result



    def generate_segmented_image(self):
        _label_image, _label_no = self.generate_label_image()
        color_list = [self.random_color(i) for i in range(_label_no)]
        _segmented_image = np.zeros(shape=self.image.shape, dtype=np.uint8)
        for y in range(self.image_height):
            for x in range(self.image_width):
                _label = _label_image[y, x]
                color = color_list[_label]
                _segmented_image[y, x] = color
        self._segmented_image = _segmented_image
        return self._segmented_image

    @property
    def label_image(self):
        if self._label_image is not None:
            return self._label_image
        _label_image, _label_no = self.generate_label_image()
        return _label_image

    @property
    def label_no(self):
        if self._label_no is not None:
           return self._label_no
        _label_image, _label_no = self.generate_label_image()
        return _label_no

    @property
    def segmented_image(self):
        if self._segmented_image is not None:
           return self._segmented_image
        _segmented_image = self.generate_segmented_image()
        return _segmented_image


def show_image(image, win_name='input image'):
    cv.namedWindow(win_name, cv.WINDOW_NORMAL)
    cv.imshow(win_name, image)
    cv.waitKey(0)
    cv.destroyAllWindows()
    return


if __name__ == '__main__':
    # image_path = r'D:\\task\\5.png'
    start = time.perf_counter()
    image_path = str(input('请输入：'))
    g = Graph(image_path=image_path)
    show_image(g.segmented_image)
    end = time.perf_counter()
    print('Running time: %s Seconds' % (end - start))


