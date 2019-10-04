import sys
import os 
curPath = os.path.abspath(__file__)
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
import numpy as np

class NetDistance(object):

    def __init__(self, net_array = []):
        self.net_distance = net_array
        # node 个数 多了一个0 节点
        self.node_count = net_array.shape[0]
        
        # 把邻接矩阵中 为0 的位置全部换位 inf 无无穷大
        self.net_distance[ np.where( self.net_distance == 0 ) ] = float("inf")


    def node_distance(self, original_node = 0 ):
        if original_node == 0:
            print("请输入大于0 的节点")
            return
        book = np.zeros(self.node_count)
        dist = self.net_distance[original_node]
        book[original_node] = 1

        for i in range(1: self.node_count):
            



def all_node_distande(net_array=[]):
    pass


def net_diameter(net_array=[]):
    pass


def average_path_length(net_array=[]):
    pass


