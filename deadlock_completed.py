import numpy as np
import queue
from collections import defaultdict

def find_loop(v, visited, vertices_visited, graph):
    visited[v] = True
    vertices_visited[v] = True

    for i in graph[v]:
        if visited[i] == False:
            if find_loop(i, visited, vertices_visited, graph) == True:
            	return True
        elif vertices_visited[i] == True:
        	return True
 
    vertices_visited[v] = False
    return False
 
def detect_deadlock(graph, V):
	visited = [False] * (V + 1)
	vertices_visited = [False] * (V + 1)
	for verices in range(V):
		if visited[verices] == False:
			if find_loop(verices,visited,vertices_visited, graph) == True:
				return vertices_visited
	return False

def run_detection(matrix, processes, n):
	graph = defaultdict(list)
	for i in range(n):
		for j in range(n):
			if matrix[i][j] == 1:
				graph[i].append(j)

	deadlock_Detected = detect_deadlock(graph, n)
	resources = ''
	processes_str = ''
	if deadlock_Detected:
		for i in range(len(deadlock_Detected)):
			if (deadlock_Detected[i] == True) and (i > max(processes)):
				resources = resources + str(i-max(processes)) + ','
			elif (deadlock_Detected[i] == True) and (i <= max(processes)):
				processes_str = processes_str + str(i) + ','
		print(f'''DEADLOCK DETECTED: Processes {processes_str} and Resources {resources} are found in a cycle.''')
		exit()

file = input("Enter the file path : ")

with open(file, 'r') as f:
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
		print(f'''Process {processes[i]} needs resource {resources[i]-max(processes)} -- Resources {resources[i]-max(processes)} is allocated to process {processes[i]}''')
		run_detection(matrix, processes, n)
	elif need_release[i] == 'N' and resource_map[resources[i]] == 1:		
		matrix[resources[i]][processes[i]] = 1
		if resources[i] not in priority_map:
			priority_map[resources[i]] = [processes[i]]
		else:
			priority_map[resources[i]].append(processes[i])
		print(f'''Process {processes[i]} needs resource {resources[i]-max(processes)} -- Process {processes[i]} must wait''')
		run_detection(matrix, processes, n)
	elif need_release[i] == 'R':
		matrix[processes[i]][resources[i]] = 0
		resource_map[i] = 0
		if resources[i] in priority_map.keys() and len(priority_map[resources[i]]) !=0:
			proc = priority_map[resources[i]].pop(0)
			matrix[resources[i]][proc] = 0
			matrix[proc][resources[i]] = 1
			print(f'''Process {processes[i]} releases resource {resources[i]-max(processes)} -- Resources {resources[i]-max(processes)} is allocated to process {proc}''')
			run_detection(matrix, processes, n)
			
		else:
			print(f'''Process {processes[i]} releases resource {resources[i]-max(processes)} -- Resource {resources[i]-max(processes)} is now free''')

print("EXECUTION COMPLETED: No deadlock encountered.")