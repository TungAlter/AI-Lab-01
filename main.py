
#! 0: BFS, 1: DFS, 2: UCS, 3: IDS, 4: GBFS, 5: A*, and 6: HC
import heapq as hq
class Path():
    def __init__(self,source,destination):
        self.source = source
        self.destination = destination
    
    def add_level(self,level):
        self.level = level
    
    def add_cost(self,cost):
        self.cost = cost

    #! defining comparators less_than and equals
    def __lt__(self, other):
        return self.destination < other.destination

    def __eq__(self, other):
        return self.destination < other.destination
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
    
    def findPath_PQ(self,expanded,init,a):
        path = []
        expanded.append(a)
        current = a.destination
        for i in range(len(expanded)-1,-1,-1):
            if(expanded[i].destination == current):
                path.append(current)
                current = expanded[i].source
            if(current == init):
                path.append(current)
                path.reverse()
                break
        return path

    def update_PQ(self,PQ,a):
        check = False
        isExisting = False
        for i in range(len(PQ)):
            if(PQ[i][1].destination == a.destination):
                isExisting = True
                if(PQ[i][1].cost > a.cost):
                    PQ.pop(i)
                    hq.heappush(PQ,(a.cost,a))
                    check = True
                    return check
                else:
                    return False
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
            expanded_list.append(expanded[i].destination)
        if(keepGoal == False and len(expanded_list) != 1):
            expanded_list.pop()
        return expanded_list

    def isExpanded(self,expanded,next_node,init):
        for i in range(len(expanded)):
            if(expanded[i].source == init):
                if(expanded[i].destination == next_node):
                    return True
            if(expanded[i].source == next_node):
                return True
        return False

    def isReached(self,frontier,next_node):
        for i in range(len(frontier)):
            if (frontier[i].destination == next_node):
                return True
        return False

    def isReached_PQ(self,frontier,next_node):
        for i in range(len(frontier)):
            if (frontier[i][1].destination == next_node):
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
                    if(self.isExpanded(expanded,next_node,init) == False and self.isReached(queue,next_node) == False):
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
        
    def DLS(self,init,goal,limit):
        expanded = []
        frontier = []
        stack = []
        curr = Path(init,init)
        curr.add_level(0)
        stack.append(curr)
        while len(stack) > 0:
            curr = stack.pop()
            expanded.append(curr)
            current_node = curr.destination
            for next_node in range(self.num_vertices - 1,-1,-1):
                #! Nếu node tiếp theo là goal thì return 
                if(self.cost_table[current_node][next_node] != 0 and next_node == goal):
                    if(curr.level < limit):
                        temp = Path(current_node, next_node)
                        expanded.append(temp)
                        self.writeExpandedList(self.getExpandList(expanded,False))
                        self.writePath(self.findPath(expanded,init,goal),True)
                        return True
                #! Nếu node tiếp theo không là goal
                if(self.cost_table[current_node][next_node] != 0 and next_node != goal):
                    if(curr.level < limit):
                        if(self.isExisting(expanded,init,current_node,next_node) == False):
                            temp = Path(current_node,next_node)
                            temp.add_level(curr.level + 1)
                            stack.append(temp)
        self.writeExpandedList(self.getExpandList(expanded,False))
        self.writePath(expanded,False)
        return False

    def IDS(self,init,goal):
        infinity = len(self.cost_table) - 1
        for i in range(infinity):
            if(self.DLS(init,goal,i) == True):
                break
        
    def GBFS(self,init,goal):
        expanded = []
        p_queue = []
        curr = Path(init,init)
        h_value = self.h_table[init]
        curr.add_cost(h_value)
        hq.heappush(p_queue,(curr.cost,curr)) 
        while(len(p_queue) > 0):
            temp = hq.heappop(p_queue)
            curr = temp[1]
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
                    if(self.isExpanded(expanded,next_node,init) == False and self.isReached_PQ(p_queue,next_node) == False):
                        temp = Path(current_node,next_node)
                        h_value = self.h_table[next_node]
                        temp.add_cost(h_value)
                        hq.heappush(p_queue,(temp.cost,temp))
        self.writeExpandedList(self.getExpandList(expanded,False))
        self.writePath(expanded,False)
        return False

    def UCS(self,init,goal):
        expanded = []
        p_queue = []
        curr = Path(init,init)
        curr.add_cost(0)
        hq.heappush(p_queue,(curr.cost,curr)) 
        while(len(p_queue) > 0):
            temp = hq.heappop(p_queue)
            curr = temp[1]
            expanded.append(curr)
            current_node = curr.destination
            #! Nếu node hiện tại là goal thì return 
            if(current_node == goal):
               self.writeExpandedList(self.getExpandList(expanded,True))
               self.writePath(self.findPath(expanded,init,goal),True)
               return True

            for next_node in range(self.num_vertices):
                #! Nếu node tiếp theo không là goal
                if(self.cost_table[current_node][next_node] != 0 and self.isExpanded(expanded,next_node,init) == False):
                    temp = Path(current_node,next_node)
                    newPath = self.findPath_PQ(expanded.copy(),init,temp)
                    cost = self.CalculateCost(newPath)
                    temp.add_cost(cost)
                    self.update_PQ(p_queue,temp)
        self.writeExpandedList(self.getExpandList(expanded,True))
        self.writePath(expanded,False)
        return False
    
    def AStar(self,init,goal):
        expanded = []
        p_queue = []
        curr = Path(init,init)
        curr.add_cost(0)
        hq.heappush(p_queue,(curr.cost,curr)) 
        while(len(p_queue) > 0):
            temp = hq.heappop(p_queue)
            curr = temp[1]
            expanded.append(curr)
            current_node = curr.destination
            #! Nếu node hiện tại là goal thì return 
            if(current_node == goal):
               self.writeExpandedList(self.getExpandList(expanded,True))
               self.writePath(self.findPath(expanded,init,goal),True)
               return True
            for next_node in range(self.num_vertices):
                #! Nếu node tiếp theo không là goal
                if(self.cost_table[current_node][next_node] != 0 and self.isExpanded(expanded,next_node,init) == False):
                    temp = Path(current_node,next_node)
                    newPath = self.findPath_PQ(expanded.copy(),init,temp)
                    cost = self.CalculateCost(newPath) + self.h_table[next_node]
                    temp.add_cost(cost)
                    self.update_PQ(p_queue,temp)
        self.writeExpandedList(self.getExpandList(expanded,True))
        self.writePath(expanded,False)
        return False
    
    def HC(self,init,goal):
        expanded = []
        neighbors = []
        curr = Path(init,init)
        while(True):
            expanded.append(curr)
            current_node = curr.destination
            if(current_node == goal):
               self.writeExpandedList(self.getExpandList(expanded,True))
               self.writePath(self.findPath(expanded,init,goal),True)
               return True
            for next_node in range(self.num_vertices):
                if(self.cost_table[current_node][next_node] != 0 and next_node == goal):
                    temp = Path(current_node,next_node)
                    neighbors.clear()
                    neighbors.append(temp)
                    break
                #! Nếu node tiếp theo không là goal
                if(self.cost_table[current_node][next_node] != 0 and self.isExpanded(expanded,next_node,init) == False):
                    temp = Path(current_node,next_node)
                    cost = self.cost_table[current_node][next_node] + self.h_table[next_node]
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
        init = lines[1][0]
        goal = lines[1][1]
        alg_index = lines[1][2]
        cost_table = []
        for i in range(2,len(lines)-1):
            cost_table.append(lines[i])
        h_table = lines[len(lines)-1]

    #! call algorithm base on the value of variable alg_index
    A = Graph(cost_table,h_table,num_vertices)
    if(alg_index == 0):
        A.BFS(init,goal)
    elif(alg_index == 1):
        A.DFS(init,goal)
    elif(alg_index == 2):
        A.UCS(init,goal)
    elif(alg_index == 3):
        A.IDS(init,goal)
    elif(alg_index == 4):
        A.GBFS(init,goal)
    elif(alg_index == 5):
        A.AStar(init,goal)
    elif(alg_index == 6):
        A.HC(init,goal)

if __name__ == "__main__":
     main()




