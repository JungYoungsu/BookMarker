resultTXT = open('result.txt', 'r')
newTXT = open('new.txt', 'w')

total = 184

numofplace = 75

line = resultTXT.readline()
place = int(line)
count = 0
num = 0

line = resultTXT.readline()
while line:
	if (num != place):
		print count
		num = place
		count = 0
	else:
		count += 1
	
	list = [-130] * (total + 1)
	list.extend( [0] * numofplace )
	list[0] = 1
	
	list[total + place] = 1
	while True:
		str = resultTXT.readline()
		arr = str.split('@')
		if (len(arr) == 1):
			place = int(arr[0])
			break
		list[int(arr[0])+1] = int(arr[1])
		
	for i, s in enumerate(list):
		newTXT.write("%s " % s)
	
	newTXT.write("\n")
	line = resultTXT.readline()

resultTXT.close()
newTXT.close()