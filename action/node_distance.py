import sys
import os 
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
import numpy as np
from analysis.data_reader import DataReader 

class NetDistance(object):

    def __init__(self, net_array = []):
        # self.net_array 主要用在 bfs 计算 直径和 。。。上
        self.net_array = net_array
        self.net_distance = net_array
        # node 个数 多了一个0 节点
        self.node_count = net_array.shape[0]
        
        # 把邻接矩阵中 为0 的位置全部换位 inf 无无穷大
        self.net_distance[ np.where( self.net_distance == 0 ) ] = float("inf")

        # result_net_distance 本来是要保存 使用 dijkstra 计算出来的所有节点之间的最短路径， 但是时间复杂度太高，计算时间太长，所以现在基本没用
        self.result_net_distance = self.net_distance
        self.is_all_node_distance_caculated = False

    # 使用 dijkstral 算法 计算 单源最短路径
    def node_distance(self, original_node = 0 ):
        if original_node == 0:
            print("请输入大于 0 的节点")
            return
        book = np.zeros(self.node_count)
        dist = self.net_distance[original_node]
        book[original_node] = 1

        #算法核心语句
        for _ in range(1, self.node_count):
            min = float("inf")
            min_index = 0
            for j in range(1, self.node_count):
                if book[j] == 0 and dist[j] < min:
                    min = dist[j]
                    min_index = j
            book[min_index] = 1
            
            for v in range(1, self.node_count):
                if self.net_distance[min_index][v] < float("inf") and book[v] == False and dist[v] > dist[min_index] + self.net_distance[min_index][v]:
                    dist[v] =  dist[min_index] + self.net_distance[min_index][v]
        return dist

    #这里暂时先使用 dijkstra 算法得出的结果
    #计算两点间的最短路径长度
    def between_distance(self, source, target):
        source_dist = self.node_distance( source )
        return source_dist[ target ]

    #暂时现不用看这个函数
    def all_node_distance(self):
        if self.is_all_node_distance_caculated == False:
            for i in range(1, self.node_count):
                self.result_net_distance[i] = self.node_distance( i )
            self.is_all_node_distance_caculated = True
        return

    # 使用 dijkstra 计算 网络直径 发现 太慢了 所以暂时不用看这个函数
    def net_diameter(self):
        if self.is_all_node_distance_caculated == False:
            self.all_node_distance()
        
        # 先取出所有不是无穷大的距离
        # 然后在这些距离中取最大值，为网络的直径
        return np.max( self.result_net_distance[ np.where( self.result_net_distance != float("inf") ) ] )


    def average_path_length(self):
        pass


    # 使用 广度优先遍历计算网络的 直径和节点间的距离
    # source 表示 从那个节点开始 是 list []
    def _single_shortest_path_length_bfs(self, source):
        seen = {}
        level = 0
        next_list = source

        while next_list != []:
            current = next_list
            next_list = []
            for v in current:
                if v not in seen:
                    seen[v] = level
                    for i in np.where( self.net_array[v] == 1 )[0]:
                        if i not in next_list:
                            next_list.append(i)
                    yield (v, level)
            level += 1
        del seen

    def single_shortest_path_length_bfs(self, source):
        return dict(self._single_shortest_path_length_bfs(source))

    # 网络的直径为 11
    def diameter_bfs(self):
        # 记录距离节点 i 最远的节点的 路径长度
        node_diameter = []
        for i in range(1, self.node_count): 
            nodelevel_dict = self.single_shortest_path_length_bfs([i])
            mid = max( nodelevel_dict.values() )
            node_diameter.append( mid )
            print(i,mid)
        return max(node_diameter)

    # (sum of all pair distance) / (n*(n-1)) 
    # 在计算 所有节点间距离的时候 我们 重复计算了  1 -> 16   16 -> 1
    # result = 4.273095287093869
    def average_path_length_bfs(self):
        total_distance = 0
        for i in range(1, self.node_count):
            nodelevel_dict = self.single_shortest_path_length_bfs([i])
            total_distance += sum(nodelevel_dict.values())
            print(total_distance)
        # 我们的数组存在 0 行 0 列
        return total_distance / ( self.node_count - 1 ) * ( self.node_count - 2 )
    

    def all_pair_node_distance(self):
        all_dict = dict()
        for i in range(1, self.node_count):
            nodelevel_dict = self.single_shortest_path_length_bfs([i])
            all_dict.update({i:nodelevel_dict})
            print(nodelevel_dict)
        return all_dict

if __name__ == "__main__":
    reader = DataReader()
    net_array = reader.data_reader()
    net_distance = NetDistance(net_array)

    # node_dist = net_distance.node_distance(1)
    # print(node_dist)
    # node_dist[ np.where(node_dist==float("inf")) ] = -1
    # print(np.max(node_dist))
    # print(np.where(node_dist == 7))

    # 测试网络直径
    # diameter = net_distance.net_diameter()

    #测试 bfs
    #为什么广搜 可以遍历到 节点3 但是 dijskral 找不到最短路径
    # s = net_distance.single_shortest_path_length_bfs([1])
    # print(max(s.values()))

    #测试 bfs 计算的 diameter
    # print(net_distance.diameter_bfs())

    #测试所有节点间的距离
    print(net_distance.average_path_length_bfs())
