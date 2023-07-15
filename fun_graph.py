import numpy as np
import xiangsu
import math
gery = xiangsu.dst_gery
var = np.var(gery)
print(var)
# 求所有灰度值的方差


def ask_weight(f1, f2, var=var):
    cha = f1-f2
    k = cha**2
    k = k/var
    weight = math.exp(-k)
    return weight
# 这个是根据灰度来求图的权值


height = xiangsu.height
width = xiangsu.width
length = xiangsu.height*xiangsu.width
# 得到全部像素点的个数



# 开始创建邻接表：第一步，定义数据结构，第二步，将path算出来的值导入记录，第三步，输出
class Vert(object):
    def __init__(self, name):
        self.name = name
        self.firstarc = None
# 创建结点类型,name存储对应的结点名称，firstarc存储第一条边


class ArcNode(object):
    def __init__(self, name,weight):
        self.next = None
        self.adjVex = name
        self.weight = weight
# 创建边类型，name存储的是每一条边的弧头名称，data存储的是这条边的权值，next存储的是下一条边的信息


class Graph(object):
    def __init__(self, vers, arcs):
        self.vers = vers
        self.arcs = arcs
        self.ver_number = len(self.vers)
        self.vertlist = [Vert for i in range(self.ver_number)]
        for i in range(self.ver_number):
            self.vertlist[i] = Vert(self.vers[i])
        for edge in self.arcs:
            c1 = edge[0]
            c2 = edge[1]
            quan = edge[2]
            self.__addArc(c1, c2,quan)

    def __addArc(self, c1, c2,quan):
        p1 = self.__getPosition(c1)
        p2 = self.__getPosition(c2)
        arcnode1 = ArcNode(p1,quan)
        arcnode2 = ArcNode(p2,quan)
        if self.vertlist[p1].firstarc is None:
            self.vertlist[p1].firstarc = arcnode2
        else:
            self.__LinkLast(self.vertlist[p1],arcnode2)

        if self.vertlist[p2].firstarc is None:
            self.vertlist[p2].firstarc = arcnode1
        else:
            self.__LinkLast(self.vertlist[p2], arcnode1)

    def __getPosition(self, key):
            for i in range(self.ver_number):
                if self.vers[i] == key:
                    return i

    def __LinkLast(self, list, arc):
        p = list.firstarc
        while p.next:
            p = p.next
        p.next = arc

    def print(self):
        for i in range(self.ver_number):
            print(self.vertlist[i].name, end="->")
            arc = self.vertlist[i].firstarc
            while arc:
                print(self.vertlist[arc.adjVex].name, end=" ")
                print(arc.weight, end=" ")
                arc = arc.next
            print()
if __name__ == "__main__":
    """
    vers=vers
    arcs=arcs
    g = Graph(vers,arcs)
    g.print()
    """