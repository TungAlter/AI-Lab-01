
#! 0: BFS, 1: DFS, 2: UCS, 3: IDS, 4: GBFS, 5: A*, and 6: HC

class Node():
    def __init__(self,index,h_value):
        self.index = index
        self.h_value = h_value
        self.adj_list = []

    def add_adj(self,adj_index):
        self.adj_list.append(adj_index)
class Graph():
    def __init__(self,cost_table,h_table,num_vertices):
        self.cost_table = cost_table
        self.h_table = h_table
        self.num_vertices = num_vertices
        self.node_list = []

        #! add node
        for i in range(num_vertices):
            temp = Node(i,h_table[i])
            self.node_list.append(temp)
        
        #! add adj vertices of each node
        for i in range(num_vertices):
            for j in range(num_vertices):
                if(self.cost_table[i][j] != 0):
                    self.node_list[i].add_adj(j)
    
    def get_cost(self,i,j):
        return self.cost_table[i][j]

    def printGraph(self):
        size = len(self.node_list)
        for i in range(size):
            print("vertice "+ str(i) + " adj: ",end = "")
            print(self.node_list[i].adj_list)   
    
#! main function
with open('input.txt') as file_object:
    lines = file_object.readlines()
    for i in range(len(lines)):
        lines[i] = lines[i].split()
        lines[i] = list(map(int, lines[i]))
    num_vertices = lines[0][0]
    init = lines[1][0]
    goal = lines[1][1]
    alg_index = lines[1][2]
    cost_table = []
    for i in range(2,len(lines)-1):
        cost_table.append(lines[i])
    h_table = lines[len(lines)-1]

A = Graph(cost_table,h_table,num_vertices)
A.printGraph()



