import trans
import xiangsu
arcs = trans.arcs
height = xiangsu.height
width = xiangsu.width
print(arcs[0])


def find(x, pres):
    """
    查找x的最上级（首级）
    :param x: 要查找的数
    :param pres: 每个元素的首级
    :return: 根结点（元素的首领结点）
    """
    root, p = x, x  # root:根节点， p:指针
    print(root)
    # 找根节点
    while root != pres[root]:
        root = pres[root]

    # 路径压缩，把每个经过的结点的上一级设为root（直接设为首级）
    while p != pres[p]:
        p, pres[p] = pres[p], root
    print(root)
    return root


def join(x, y, pres, n):
    """
    合并两个元素（合并两个集合）
    :param x: 第一个元素
    :param y: 第二个元素
    :param pres: 每个元素的上一级
    :return: None
    """
    h1, h2 = find(x, pres), find(y, pres)
    # 当两个元素不是同一组的时候才合并
    list = [h1,h2]
    list.sort()
    min = list[0]
    max = list[1]
    print(min,max)
    if h1 != h2:
        if h1 < h2:
            pres[h2] = h1
        else:
            pres[h1] = h2
    for i in range(n):
        if pres[i] == max:
            pres[i] = min


n = height*width


def kruskal(n, arcs):
    """
    kruskal算法
    :param n: 结点数
    :param arcs: 带权边集
    :return: 构成最小生成树的边集
    """
    # 初始化：pres一开始设置每个元素的上一级是自己
    print("边是")
    pres = [e for e in range(n)]
    print(pres)
    # 边从大到小排序
    edges = sorted(arcs, key=lambda x: x[-1])
    mst_edges, num = [], 0
    for edge in edges:
        if find(edge[0], pres) != find(edge[1], pres):
            mst_edges.append(edge)
            join(edge[0], edge[1], pres,n)
            num += 1
        else:
            continue
    return pres


pres = kruskal(n,arcs)
pres_2 = list(set(pres))
length = len(pres_2)    # pres代表的是root值，pres_2代表的是去掉重复值的结果
print(length)
print(pres)
print(pres_2)
"""
all = []    # 最后得到的结果，按照二维数组进行存储
for i in range(length):
    part = []   # 不同的划分
    for j in range(n):  # 相同的划分存储到一起
        if pres[j] == pres_2[i]:
            part.append(arcs[j])
    all.append(part)
    print(part)
print(all)
"""