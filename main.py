
#! 0: BFS, 1: DFS, 2: UCS, 3: IDS, 4: GBFS, 5: A*, and 6: HC


class Path():
    def __init__(self,source,destination):
        self.source = source
        self.destination = destination
class Graph():
    def __init__(self,cost_table,h_table,num_vertices):
        self.cost_table = cost_table
        self.h_table = h_table
        self.num_vertices = num_vertices        

    def findPath(self,expanded,init,goal):
        path = []
        current = goal
        for i in range(len(expanded)-1,-1,-1):
            if(expanded[i].destination == current):
                path.append(current)
                current = expanded[i].source
            if(current == init):
                path.append(current)
                path.reverse()
                break
        print("path found: ",path)

    def getExpandList(self,expanded):
        expanded_list = []
        for i in range(len(expanded)):
            expanded_list.append(expanded[i].destination)
        print(expanded_list)

    def isExpanded(self,expanded,next_node):
        for i in range(len(expanded)):
            if(expanded[i].source == next_node):
                return True
        return False

    def isExist(self,frontier,next_node):
        if(len(frontier)==0):
            return False
        for i in range(len(frontier)):
            if (frontier[i].destination == next_node):
                return True
        return False
            
    def BFS(self,init,goal):
        expanded = []
        frontier = []
        temp = Path(init,init)
        frontier.append(temp) 
        while(len(frontier) > 0):
            temp = frontier.pop(0)
            expanded.append(temp)
            current_node = temp.destination
            for next_node in range(self.num_vertices):
                #! Nếu node tiếp theo là goal thì return 
                if(self.cost_table[current_node][next_node] != 0 and next_node == goal):
                    temp = Path(current_node, next_node)
                    expanded.append(temp)
                    self.getExpandList(expanded)
                    self.findPath(expanded,init,goal)
                    return True
                #! Nếu node tiếp theo không là goal
                if(self.cost_table[current_node][next_node] != 0 and next_node != goal):
                    if(self.isExpanded(expanded,next_node) == False and self.isExist(frontier,next_node) == False):
                        temp = Path(current_node,next_node)
                        frontier.append(temp)
        print("Path not found")
        self.getExpandList(expanded)
                
def main():
    filename = 'input.txt'
    #! get date from file
    with open(filename) as file_object:
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
    #! test alg
    A = Graph(cost_table,h_table,num_vertices)
    A.BFS(init,goal)

if __name__ == "__main__":
     main()




