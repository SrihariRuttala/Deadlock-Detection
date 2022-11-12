import numpy as np
import queue
from collections import defaultdict
# file = input("Enter the file path : ")

def BFS(matrix, start, n):
	queue = []
	visited = [0] * n
	visited_dict = {}
	# print(visited)
	queue.append(start)
	visited[start] = 1
	visited_dict[start] = 0
	# print(str(start), " ", end="")

	while len(queue)!=0:
		u = queue.pop(0)
		for i in range(n):
			if matrix[u][i] == 1 and visited[i] == 0:
				# print(str(i), " ", end="")
				visited[i] = 1
				visited_dict[i] = 0
				queue.append(i)

	return visited_dict

def find_loop(matrix, visited_dict, n, adj):
	if visited_dict[adj] == True:
		return True
	visited_dict[adj] = 1
	deadlock_detected = False
	vertices = []
	count = 0
	print(adj)
	print(visited_dict)
	for j in range(n):
		if matrix[adj][j] == 1:
			vertices.append(j)
			count = count + 1

	for j in range(count):
		deadlock_detected = find_loop(matrix, visited_dict, n, vertices[j])
		if deadlock_detected == True:
			# print(visited_dict)
			return True
	return False

def detect_deadlock(matrix, visited_dict, n):
	deadlock_detected = False
	reStack = visited_dict
	dict_len = len(visited_dict)
	keys = list(visited_dict.keys())
	for i in range(dict_len):
		visited_dict[keys[i]] = 1
		key = keys[i]
		vertices = []
		count = 0
		for j in range(n):
			if matrix[key][j] == 1:
				vertices.append(j)
				count = count + 1
		# print(vertices)
		for j in range(count):
			deadlock_detected = find_loop(matrix, visited_dict, n, vertices[j])
			if deadlock_detected == True:
				return True
		visited_dict[keys[i]] = 0
		# print(visited_dict)

	return False

# def loop_detected(i, visited, stack, graph):
# 	visited[i] = True
# 	stack[i] = True
# 	for j in graph[i]:
# 		if visited[j] == False:
# 			if loop_detected(i, visited, stack, graph) == True:
# 				return True
# 		elif stack[j] == True:
# 			return True
# 	stack[i] = False
# 	return False

# def detect_deadlock(graph,n):
# 	visited = [False] * n
# 	stack = [False] * n
# 	for i in range(n):
# 		if visited[i] == False:
# 			if loop_detected(i, visited, stack, graph) == True:
# 				return True
# 	return False



def isCyclicUtil(v, visited, recStack, graph):
 
    visited[v] = True
    print(v)
    recStack[v] = True

    for neighbour in graph[v]:
        if visited[neighbour] == False:
            if isCyclicUtil(neighbour, visited, recStack, graph) == True:
            	return True
        elif recStack[neighbour] == True:
        	return True
 
    recStack[v] = False
    return False
 
def isCyclic(graph, V):
	visited = [False] * (V + 1)
	recStack = [False] * (V + 1)
	for node in range(V):
		if visited[node] == False:
			if isCyclicUtil(node,visited,recStack, graph) == True:
				return recStack
	return False

with open('input3.txt', 'r') as f:
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
needs = f'''Process {processes[i]} needs resource {resources[i]} -- '''
releases = f'''"Process {processes[i]} releases resoruce {resources[i]} -- '''
allocated = f'''Resources {resources[i]} is allocated to process {processes[i]}'''
wait = f'''Process {processes[i]} must wait'''
free = f'''Resource {releases[i]} is now free'''

for i in resources:
	resource_map[i] = 0

# print(processes)
# print(resources)

for i in range(m):
	if need_release[i] == 'N' and resource_map[resources[i]] == 0:
		matrix[processes[i]][resources[i]] = 1
		resource_map[resources[i]] = 1
		print(f'''Process {processes[i]} needs resource {resources[i]-max(processes)} -- Resources {resources[i]-max(processes)} is allocated to process {processes[i]}''')
	elif need_release[i] == 'N' and resource_map[resources[i]] == 1:		
		matrix[resources[i]][processes[i]] = 1
		if resources[i] not in priority_map:
			priority_map[resources[i]] = [processes[i]]
		else:
			priority_map[resources[i]].append(processes[i])
		print(f'''Process {processes[i]} needs resource {resources[i]-max(processes)} -- Process {processes[i]} must wait''')
	elif need_release[i] == 'R':
		matrix[processes[i]][resources[i]] = 0
		resource_map[i] = 0
		if resources[i] in priority_map.keys() and len(priority_map[resources[i]]) !=0:
			proc = priority_map[resources[i]].pop(0)
			matrix[resources[i]][proc] = 0
			matrix[proc][resources[i]] = 1
			print(f'''Process {processes[i]} releases resource {resources[i]-max(processes)} -- Resources {resources[i]-max(processes)} is allocated to process {proc}''')
			
		else:
			print(f'''Process {processes[i]} releases resource {resources[i]-max(processes)} -- Resource {resources[i]-max(processes)} is now free''')

# print(matrix)
graph = defaultdict(list)
for i in range(n):
	for j in range(n):
		if matrix[i][j] == 1:
			graph[i].append(j)

# print(len(graph))

# visited_vertices = BFS(matrix, 1, n)
deadlock_Detected = isCyclic(graph, n)
# deadlock_Detected = detect_deadlock(matrix, visited_vertices, n)
resources = ''
processes_str = ''
if deadlock_Detected:
	for i in range(len(deadlock_Detected)):
		if (deadlock_Detected[i] == True) and (i > max(processes)):
			resources = resources + str(i-max(processes)) + ','
		elif (deadlock_Detected[i] == True) and (i <= max(processes)):
			processes_str = processes_str + str(i) + ','
	print(f'''DEADLOCK DETECTED: Processes {processes_str} and Resources {resources} are found in a cycle.''')
else:
	print("EXECUTION COMPLETED: No deadlock encountered.")