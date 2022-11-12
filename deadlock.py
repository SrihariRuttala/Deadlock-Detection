import numpy as np
import queue
# file = input("Enter the file path : ")

def BFS(matrix, start, n):
	queue = []
	visited = [0] * n
	visited_dict = {}
	print(visited)
	queue.append(start)
	visited[start] = 1
	visited_dict[start] = 0
	print(str(start), " ", end="")

	while len(queue)!=0:
		u = queue.pop(0)
		for i in range(n):
			if matrix[u][i] == 1 and visited[i] == 0:
				print(str(i), " ", end="")
				visited[i] = 1
				visited_dict[i] = 0
				queue.append(i)

	return visited_dict

with open('input1.txt', 'r') as f:
	data = f.readlines()
	processes = []
	need_release = []
	resources = []
	for i in range(len(data)):
		data[i] = data[i].strip()
		processes.append(int(data[i][0]))
		need_release.append(data[i][2])
		resources.append(int(data[i][4]))

n = max(resources) + max(processes) + 1
arr = []
for i in range(len(resources)):
	ele = resources[i] + max(processes) 
	arr.append(ele)

resources = arr
m = len(data)
matrix = np.full((n,n),0)
priority_map = {}
resource_map = {}

for i in resources:
	resource_map[i] = 0

for i in range(m):
	if need_release[i] == 'N' and resource_map[resources[i]] == 0:
		matrix[processes[i]][resources[i]] = 1
		resource_map[resources[i]] = 1
	elif need_release[i] == 'N' and resource_map[resources[i]] == 1:		
		matrix[resources[i]][processes[i]] = 1
		if resources[i] not in priority_map:
			priority_map[resources[i]] = [processes[i]]
		else:
			# val = list(priority_map[resources[i]][-1].values())[0] + 1
			priority_map[resources[i]].append(processes[i])
	elif need_release[i] == 'R':
		matrix[processes[i]][resources[i]] = 0
		resource_map[i] = 0
		if resources[i] in priority_map.keys():
			print(priority_map[resources[i]])
			proc = priority_map[resources[i]].pop(0)
			matrix[resources[i]][proc] = 0
			matrix[proc][resources[i]] = 1

vertices = BFS(matrix, 6, n)