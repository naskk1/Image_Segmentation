import xiangsu
import fun_graph
import math

height = xiangsu.height
width = xiangsu.width
grey = xiangsu.dst_gery
vers = []
arcs = []

for i in range(0,height):
    for j in range(0,width):
        index = i*height+j
        vers.append(index)
# 以上是将矩阵对应的点转换为结点名称


var = fun_graph.var


def ask_weight(f1, f2, var=var):
    cha = f1-f2
    k = cha**2
    k = k/var
    weight = math.exp(-k)
    return weight


def ask_name(i,j):
    return i*width+j


def ask_arcnode(i1,j1,i2,j2):
    """
    得到两个点之间的权值，组成一个列表
    i1: 第一个点的横坐标
    j1: 第一个点的纵坐标
    i2: 第二个点的横坐标
    j2: 第二个点的纵坐标
    return:一个[点，点，权]的列表
    """
    arcnode = []
    name1 = ask_name(i1,j1)
    arcnode.append(name1)
    name2 = ask_name(i2, j2)
    arcnode.append(name2)
    weight = ask_weight(grey[i1][j1],grey[i2][j2])
    weight = float(format(weight, '.7f'))
    arcnode.append(weight)
    return arcnode


for i in range(0,height):
    for j in range(0,width):
        if i == 0:  # 第一行，只能有右，下，右下，没有右上
            if j == width - 1:  # 最后一列，这时只能有下
                arcnode = ask_arcnode(i, j, i + 1, j)
                arcs.append(arcnode)
            else:   # 第一行除去最后一个点，可以有右，下，右下
                arcnode = ask_arcnode(i, j, i, j + 1)
                arcs.append(arcnode)
                arcnode = ask_arcnode(i, j, i + 1, j)
                arcs.append(arcnode)
                arcnode = ask_arcnode(i, j, i + 1, j + 1)
                arcs.append(arcnode)
        elif i == height-1:  # 最后一行，只能有右，右上，没有下，右下
            if j == width - 1:  # 最后一行的最后一列，这时退出
                break
            else:
                arcnode = ask_arcnode(i, j, i, j+1)
                arcs.append(arcnode)
                arcnode = ask_arcnode(i, j, i - 1, j + 1)
                arcs.append(arcnode)
        else:   # 中间部分，只要不是最后一列（只有下），其他情况都有
            if j == width - 1:  # 最后一列
                arcnode = ask_arcnode(i, j, i + 1, j)
                arcs.append(arcnode)
            else:
                arcnode = ask_arcnode(i, j, i, j + 1)
                arcs.append(arcnode)
                arcnode = ask_arcnode(i, j, i + 1, j)
                arcs.append(arcnode)
                arcnode = ask_arcnode(i, j, i + 1, j + 1)
                arcs.append(arcnode)
                arcnode = ask_arcnode(i, j, i - 1, j + 1)
                arcs.append(arcnode)


def judge(a):
    weight = a[2]
    if weight > 0.999999:
        return 1
    else:
        return 0


arcs = list(filter(judge,arcs))
arcs = sorted(arcs, key=lambda s: s[2], reverse=False)       # 按降序
# 此时地weight全为1，所以最小生成树可以说是不存在

