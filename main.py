
#! 0: BFS, 1: DFS, 2: UCS, 3: IDS, 4: GBFS, 5: A*, and 6: HC
class Path():
    def __init__(self,source,destination):
        self.source = source
        self.destination = destination
    def add_level(self,level):
        self.level = level
    def add_cost(self,cost):
        self.cost = cost
class Graph():
    def __init__(self,cost_table,h_table,num_vertices):
        self.cost_table = cost_table
        self.h_table = h_table
        self.num_vertices = num_vertices        

    def writePath(self,path,isFound):
        filename = "output.txt"
        with open(filename,'a') as f:
            if(isFound == False):
                f.write("No path")
            else:
                path = list(map(str,path))
                for i in range(len(path)):
                    f.write(path[i])
                    f.write(" ")

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
        return path
    
    def writeExpandedList(self,expanded_list):
        filename = "output.txt"
        with open(filename, 'w') as f:
            expanded_list = list(map(str,expanded_list))
            for i in range(len(expanded_list)):
                f.write(expanded_list[i])
                f.write(" ")
            f.write("\n")

    def getExpandList(self,expanded,keepGoal):
        expanded_list = []
        for i in range(len(expanded)):
            expanded_list.append(expanded[i].destination)
        if(keepGoal == False and len(expanded_list) != 1):
            expanded_list.pop()
        return expanded_list

    def isExpanded(self,expanded,next_node):
        for i in range(len(expanded)):
            if(expanded[i].source == next_node):
                return True
        return False

    def isReached(self,frontier,next_node):
        for i in range(len(frontier)):
            if (frontier[i].destination == next_node):
                return True
        return False

    def isExisting(self,expanded,init,current_node,next_node):
        path = self.findPath(expanded,init,current_node)
        for i in range(len(path)):
            if (path[i] == next_node):
                return True
        return False

    def BFS(self,init,goal):
        expanded = []
        queue = []
        curr = Path(init,init)
        queue.append(curr) 
        while(len(queue) > 0):
            curr = queue.pop(0)
            expanded.append(curr)
            current_node = curr.destination
            for next_node in range(self.num_vertices):
                #! Nếu node tiếp theo là goal thì return 
                if(self.cost_table[current_node][next_node] != 0 and next_node == goal):
                    temp = Path(current_node, next_node)
                    expanded.append(temp)
                    self.writeExpandedList(self.getExpandList(expanded,False))
                    self.writePath(self.findPath(expanded,init,goal),True)
                    return True
                #! Nếu node tiếp theo không là goal
                if(self.cost_table[current_node][next_node] != 0 and next_node != goal):
                    if(self.isExpanded(expanded,next_node) == False and self.isReached(queue,next_node) == False):
                        temp = Path(current_node,next_node)
                        queue.append(temp)
        self.writeExpandedList(self.getExpandList(expanded,False))
        self.writePath(expanded,False)
        return False
    
    def DFS(self,init,goal):
        expanded = []
        stack = []
        curr = Path(init,init)
        stack.append(curr)
        while len(stack) > 0:
            curr = stack.pop()
            expanded.append(curr)
            current_node = curr.destination
            for next_node in range(self.num_vertices - 1,-1,-1):
                #! Nếu node tiếp theo là goal thì return 
                if(self.cost_table[current_node][next_node] != 0 and next_node == goal):
                    temp = Path(current_node, next_node)
                    expanded.append(temp)
                    self.writeExpandedList(self.getExpandList(expanded,False))
                    self.writePath(self.findPath(expanded,init,goal),True)
                    return True
                #! Nếu node tiếp theo không là goal
                if(self.cost_table[current_node][next_node] != 0 and next_node != goal):
                    if(self.isExisting(expanded,init,current_node,next_node) == False):
                        temp = Path(current_node,next_node)
                        stack.append(temp)
        self.writeExpandedList(self.getExpandList(expanded,False))
        self.writePath(expanded,False)
        return False
        
    # def DLS(self,init,goal,limit):
    #     expanded = []
    #     frontier = []
    #     stack = []
    #     curr = Path(init,init)
    #     curr.add_level(0)
    #     stack.append(curr)
    #     while len(stack) > 0:
    #         curr = stack.pop()
    #         expanded.append(curr)
    #         current_node = curr.destination
    #         for next_node in range(self.num_vertices - 1,-1,-1):
    #             #! Nếu node tiếp theo là goal thì return 
    #             if(self.cost_table[current_node][next_node] != 0 and next_node == goal):
    #                 temp = Path(current_node, next_node)
    #                 expanded.append(temp)
    #                 self.getExpandList(expanded,False)
    #                 self.findPath(expanded,init,goal)
    #                 return True
    #             #! Nếu node tiếp theo không là goal
    #             if(self.cost_table[current_node][next_node] != 0 and next_node != goal):
    #                 if(curr.level < limit):
    #                     if(self.isExisting(expanded,init,current_node,next_node) == False):
    #                         temp = Path(current_node,next_node)
    #                         temp.add_cost(curr.cost + 1)
    #                         stack.append(temp)
    #     print("Path not found")
    #     self.getExpandList(expanded,False)
    #     return False

    #def IDS(self,init,goal):

        

                
def main():
    filename = 'input1.txt'
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
    if(alg_index == 0):
        A.BFS(init,goal)
    elif(alg_index == 1):
        A.DFS(init,goal)

if __name__ == "__main__":
     main()




