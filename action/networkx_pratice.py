import networkx as nx 
import os
import sys
import matplotlib.pyplot as plt 
import numpy as np 

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from analysis.data_reader import DataReader 
from node_distance import NetDistance


def create_graph(file_path="./../data/web-edu.mtx"):
    
    if os.path.exists(file_path):
        G = nx.Graph()
        with open(file_path) as f:
            lines = f.readlines()[2:]
            for line in lines:
                head, tail = [int(x) for x in line.split()]
                G.add_edge(head,tail)
        
        return G
    else:
        print("数据文件不存在")
        return 


# 对比一下 networkx 和 自己编写的 函数的结果是否相同
def compare():
    G = create_graph()
    # print(G.degree(1))
    # path = nx.dijkstra_path(G, 1, 1200)
    # print(path)
    # nx.draw(G)
    # plt.title("graph")
    # plt.axis('on') 
    # plt.xticks([]) 
    # plt.yticks([])
    # plt.show()

    dist1 = np.zeros( G.number_of_nodes() + 1 )
    
    for i in range(1, G.number_of_nodes() + 1):
        dist1[i] = nx.dijkstra_path_length(G, 2, i)

    print(np.max(dist1))
    print(np.min(dist1))

    reader = DataReader()
    net_array = reader.data_reader()
    net_distance = NetDistance(net_array)
    node_dist1 = net_distance.node_distance(2)
    node_dist1[ np.where(node_dist1==float("inf")) ] = 0
    print(np.max(node_dist1))
    # print(np.where(node_dist == 7))

    print(dist1.size, node_dist1.size)

    print(np.where( dist1 == node_dist1))


if __name__ == "__main__":
    G = create_graph()
    # print(nx.diameter(G))
    # print(nx.average_shortest_path_length(G))
    # print(G.order())
    # print( max(dict(nx.all_pairs_shortest_path_length(G))[1].values()) )

    # dist1 = np.zeros( G.number_of_nodes() + 1 )
    
    # for i in range(1, G.number_of_nodes() + 1):
    #     dist1[i] = nx.dijkstra_path_length(G, 2, i)

    # print(dist1)
    # print(np.where(dist1 == 0))


    reader = DataReader()
    net_array = reader.data_reader()
    net_distance = NetDistance(net_array)
    node_dist1 = net_distance.node_distance(1)

    print(node_dist1)
    print(np.where(node_dist1 == float("inf")))
    # print(nx.average_shortest_path_length(G))

    #判断网络是否联通
    print(nx.is_connected(G))
    path = nx.dijkstra_path(G, 1, 2)
    print(path)

    dist1 = np.zeros( G.number_of_nodes() + 1 )
    
    for i in range(1, G.number_of_nodes() + 1):
        dist1[i] = nx.dijkstra_path_length(G, 1, i)

    print(np.where(dist1 == 0))

    # reader = DataReader()
    # net_array = reader.data_reader()
    # net_distance = NetDistance(net_array)
    # node_dist1 = net_distance.node_distance(2)

    # print(node_dist1)
    # print(np.where(node_dist1 == float("inf")))
    # print(nx.average_shortest_path_length(G))

