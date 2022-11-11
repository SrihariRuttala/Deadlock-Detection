


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

if max(processes) < max(resources):
	n = max(resources)
else:
	n = max(processes)

m = len(data)

matrix = [[0]*n] * n

for i in range(m):
	if need_release == 'N' and m[]