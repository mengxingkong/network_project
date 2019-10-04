import networkx as nx 
import os
import matplotlib.pyplot as plt 

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
    


if __name__ == "__main__":

    G = create_graph()
    print(G.degree(1))

    path = nx.dijkstra_path(G, 1, 1200)
    print(path)
    # nx.draw(G)
    # plt.title("graph")
    # plt.axis('on') 
    # plt.xticks([]) 
    # plt.yticks([])
    # plt.show()



