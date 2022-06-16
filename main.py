
#! 0: BFS, 1: DFS, 2: UCS, 3: IDS, 4: GBFS, 5: A*, and 6: HC

with open('input.txt') as file_object:
    lines = file_object.readlines()

for i in range(len(lines)):
    lines[i] = lines[i].split()
    lines[i] = list(map(int, lines[i]))
print(lines)

num_vertices = lines[0][0]
init = lines[1][0]
goal = lines[1][1]
alg_index = lines[1][2]

matrix = []
for i in range(2,len(lines)-1):
    matrix.append(lines[i])

for i in range(len(matrix)):
    print(matrix[i])

