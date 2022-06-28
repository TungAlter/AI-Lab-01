
#! 0: BFS, 1: DFS, 2: UCS, 3: IDS, 4: GBFS, 5: A*, and 6: HC
import heapq as hq
class Node():
    def __init__(self,parent,index):
        self.parent = parent
        self.index = index
    
    def add_level(self,level):
        self.level = level
    
    def add_cost(self,cost):
        self.cost = cost

    #! defining comparators less than and equals
    def __lt__(self, other):
        return self.index < other.index

    def __lt__(self, other):
        return self.index < other.index
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

    def findPath(self,expanded,source,destination):
        path = []
        current = destination
        for i in range(len(expanded)-1,-1,-1):
            if(expanded[i].index == current):
                path.append(current)
                current = expanded[i].parent
            if(current == source):
                path.append(current)
                path.reverse()
                break
        return path

    def update_PQ(self,PQ,a):
        check = False
        isExisting = False
        for i in range(len(PQ)):
            if(PQ[i][1].index == a.index):
                isExisting = True
                if(PQ[i][1].cost > a.cost):
                    PQ.pop(i)
                    hq.heappush(PQ,(a.cost,a))
                    check = True
                    return check
                else:
                    return check
        if(isExisting == False):
            hq.heappush(PQ,(a.cost,a))
            check = True
        return check

    def CalculateCost(self,path):
        cost = 0
        for i in range(len(path)-1):
            j = i + 1
            current_node = path[i]
            next_node = path[j]
            cost += self.cost_table[current_node][next_node]
        return cost 

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
            expanded_list.append(expanded[i].index)
        if(keepGoal == False and len(expanded_list) != 1):
            expanded_list.pop()
        return expanded_list

    def isExpanded(self,expanded,next_node,source):
        for i in range(len(expanded)):
            if(expanded[i].parent == source):
                if(expanded[i].index == next_node):
                    return True
            if(expanded[i].parent == next_node):
                return True
        return False

    def isReached(self,frontier,next_node):
        for i in range(len(frontier)):
            if (frontier[i].index == next_node):
                return True
        return False

    def isReached_PQ(self,frontier,next_node):
        for i in range(len(frontier)):
            if (frontier[i][1].index == next_node):
                return True
        return False

    def isExisting(self,expanded,source,current_node,next_node):
        path = self.findPath(expanded,source,current_node)
        for i in range(len(path)):
            if (path[i] == next_node):
                return True
        return False

    def BFS(self,source,destination):
        expanded = []
        queue = []
        curr = Node(source,source)
        queue.append(curr) 
        while(len(queue) > 0):
            curr = queue.pop(0)
            expanded.append(curr)
            current_node = curr.index
            for next_node in range(self.num_vertices):
                #! if next node is destination node 
                if(self.cost_table[current_node][next_node] != 0 and next_node == destination):
                    temp = Node(current_node, next_node)
                    expanded.append(temp)
                    self.writeExpandedList(self.getExpandList(expanded,False))
                    self.writePath(self.findPath(expanded,source,destination),True)
                    return True
                #! if next node is not destination node 
                if(self.cost_table[current_node][next_node] != 0 and next_node != destination):
                    if(self.isExpanded(expanded,next_node,source) == False and self.isReached(queue,next_node) == False):
                        temp = Node(current_node,next_node)
                        queue.append(temp)
        self.writeExpandedList(self.getExpandList(expanded,False))
        self.writePath(expanded,False)
        return False
    
    def DFS(self,source,destination):
        expanded = []
        stack = []
        curr = Node(source,source)
        stack.append(curr)
        while len(stack) > 0:
            curr = stack.pop()
            expanded.append(curr)
            current_node = curr.index
            for next_node in range(self.num_vertices - 1,-1,-1):
                #! if next node is destination node  
                if(self.cost_table[current_node][next_node] != 0 and next_node == destination):
                    temp = Node(current_node, next_node)
                    expanded.append(temp)
                    self.writeExpandedList(self.getExpandList(expanded,False))
                    self.writePath(self.findPath(expanded,source,destination),True)
                    return True
                #! if next node is not destination node  
                if(self.cost_table[current_node][next_node] != 0 and next_node != destination):
                    if(self.isExisting(expanded,source,current_node,next_node) == False):
                        temp = Node(current_node,next_node)
                        stack.append(temp)
        self.writeExpandedList(self.getExpandList(expanded,False))
        self.writePath(expanded,False)
        return False
        
    def DLS(self,source,destination,limit):
        expanded = []
        stack = []
        curr = Node(source,source)
        curr.add_level(0)
        stack.append(curr)
        while len(stack) > 0:
            curr = stack.pop()
            expanded.append(curr)
            current_node = curr.index
            for next_node in range(self.num_vertices - 1,-1,-1):
                #! if next node is destination node 
                if(self.cost_table[current_node][next_node] != 0 and next_node == destination):
                    if(curr.level < limit):
                        temp = Node(current_node, next_node)
                        expanded.append(temp)
                        self.writeExpandedList(self.getExpandList(expanded,False))
                        self.writePath(self.findPath(expanded,source,destination),True)
                        return True
                #! if next node is not destination node 
                if(self.cost_table[current_node][next_node] != 0 and next_node != destination):
                    if(curr.level < limit):
                        if(self.isExisting(expanded,source,current_node,next_node) == False):
                            temp = Node(current_node,next_node)
                            temp.add_level(curr.level + 1)
                            stack.append(temp)
        self.writeExpandedList(self.getExpandList(expanded,False))
        self.writePath(expanded,False)
        return False

    def IDS(self,source,destination):
        infinity = self.num_vertices - 1
        for i in range(infinity):
            if(self.DLS(source,destination,i) == True):
                break
        
    def GBFS(self,source,destination):
        expanded = []
        p_queue = []
        curr = Node(source,source)
        h_value = self.h_table[source]
        curr.add_cost(h_value)
        hq.heappush(p_queue,(curr.cost,curr)) 
        while(len(p_queue) > 0):
            temp = hq.heappop(p_queue)
            curr = temp[1]
            expanded.append(curr)
            current_node = curr.index
            for next_node in range(self.num_vertices):
                #! if next node is destination node 
                if(self.cost_table[current_node][next_node] != 0 and next_node == destination):
                    temp = Node(current_node, next_node)
                    expanded.append(temp)
                    self.writeExpandedList(self.getExpandList(expanded,False))
                    self.writePath(self.findPath(expanded,source,destination),True)
                    return True
                #! if next node is not destination node 
                if(self.cost_table[current_node][next_node] != 0 and next_node != destination):
                    if(self.isExpanded(expanded,next_node,source) == False and self.isReached_PQ(p_queue,next_node) == False):
                        temp = Node(current_node,next_node)
                        h_value = self.h_table[next_node]
                        temp.add_cost(h_value)
                        hq.heappush(p_queue,(temp.cost,temp))
        self.writeExpandedList(self.getExpandList(expanded,False))
        self.writePath(expanded,False)
        return False

    def UCS(self,source,destination):
        expanded = []
        p_queue = []
        curr = Node(source,source)
        curr.add_cost(0)
        hq.heappush(p_queue,(curr.cost,curr)) 
        while(len(p_queue) > 0):
            temp = hq.heappop(p_queue)
            curr = temp[1]
            expanded.append(curr)
            current_node = curr.index
            #! if next node is destination node  
            if(current_node == destination):
               self.writeExpandedList(self.getExpandList(expanded,True))
               self.writePath(self.findPath(expanded,source,destination),True)
               return True

            for next_node in range(self.num_vertices):
            #! if next node is not destination node 
                if(self.cost_table[current_node][next_node] != 0 and self.isExpanded(expanded,next_node,source) == False):
                    temp = Node(current_node,next_node)
                    temp_expanded = expanded.copy()
                    temp_expanded.append(temp)
                    tempPath = self.findPath(temp_expanded,source,temp.index)
                    cost = self.CalculateCost(tempPath)
                    temp.add_cost(cost)
                    self.update_PQ(p_queue,temp)
        self.writeExpandedList(self.getExpandList(expanded,True))
        self.writePath(expanded,False)
        return False
    
    def AStar(self,source,destination):
        expanded = []
        p_queue = []
        curr = Node(source,source)
        curr.add_cost(0)
        hq.heappush(p_queue,(curr.cost,curr)) 
        while(len(p_queue) > 0):
            temp = hq.heappop(p_queue)
            curr = temp[1]
            expanded.append(curr)
            current_node = curr.index
            #! if next node is destination node  
            if(current_node == destination):
               self.writeExpandedList(self.getExpandList(expanded,True))
               self.writePath(self.findPath(expanded,source,destination),True)
               return True
            for next_node in range(self.num_vertices):
                #! if next node is not destination node 
                if(self.cost_table[current_node][next_node] != 0 and self.isExpanded(expanded,next_node,source) == False):
                    temp = Node(current_node,next_node)
                    temp_expanded = expanded.copy()
                    temp_expanded.append(temp)
                    tempPath = self.findPath(temp_expanded,source,temp.index)
                    cost = self.CalculateCost(tempPath) + self.h_table[next_node]
                    temp.add_cost(cost)
                    self.update_PQ(p_queue,temp)
        self.writeExpandedList(self.getExpandList(expanded,True))
        self.writePath(expanded,False)
        return False
    
    def HC(self,source,destination):
        expanded = []
        neighbors = []
        curr = Node(source,source)
        while(True):
            expanded.append(curr)
            current_node = curr.index
            if(current_node == destination):
               self.writeExpandedList(self.getExpandList(expanded,True))
               self.writePath(self.findPath(expanded,source,destination),True)
               return True
            for next_node in range(self.num_vertices):
                if(self.cost_table[current_node][next_node] != 0 and next_node == destination):
                    temp = Node(current_node,next_node)
                    neighbors.clear()
                    neighbors.append(temp)
                    break
                #! if next node is not destination node 
                if(self.cost_table[current_node][next_node] != 0 and self.isExpanded(expanded,next_node,source) == False):
                    temp = Node(current_node,next_node)
                    cost = self.h_table[next_node]
                    temp.add_cost(cost)
                    neighbors.append(temp)
            if(len(neighbors) == 0):
                break
            else:
                best_choice = neighbors[0]  
                for i in range (1,len(neighbors)):
                    if(neighbors[i].cost < best_choice.cost):
                        best_choice = neighbors[i]
                curr = best_choice
                neighbors.clear()
        self.writeExpandedList(self.getExpandList(expanded,True))
        self.writePath(expanded,False)
        return False   

def main():
    #filename = 'input1.txt'
    #filename = 'input2.txt'
    filename = 'input3.txt' 
    #! get data from file .txt
    with open(filename) as file_object:
        lines = file_object.readlines()
        for i in range(len(lines)):
            lines[i] = lines[i].split()
            lines[i] = list(map(int, lines[i]))
        num_vertices = lines[0][0]
        source = lines[1][0]
        destination = lines[1][1]
        alg_index = lines[1][2]
        cost_table = []
        for i in range(2,len(lines)-1):
            cost_table.append(lines[i])
        h_table = lines[len(lines)-1]

    #! call algorithm base on the value of variable alg_index
    A = Graph(cost_table,h_table,num_vertices)
    if(alg_index == 0):
        A.BFS(source,destination)
    elif(alg_index == 1):
        A.DFS(source,destination)
    elif(alg_index == 2):
        A.UCS(source,destination)
    elif(alg_index == 3):
        A.IDS(source,destination)
    elif(alg_index == 4):
        A.GBFS(source,destination)
    elif(alg_index == 5):
        A.AStar(source,destination)
    elif(alg_index == 6):
        A.HC(source,destination)

if __name__ == "__main__":
     main()




