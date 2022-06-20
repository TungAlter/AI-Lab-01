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

    
PQ = []
a = Path(1,2)
a.add_cost(30)
hq.heappush(PQ,(a.cost,a))
print(PQ)

b = Path(1,3)
b.add_cost(20)
hq.heappush(PQ,(b.cost,b))
print(PQ)

c = Path(2,3)
c.add_cost(10)

for i in range(len(PQ)):
    if(PQ[i][1].destination == c.destination):
        if(PQ[i][1].cost > c.cost):
            PQ.pop(i)
            break
print(PQ)