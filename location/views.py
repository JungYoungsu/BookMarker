import tensorflow as tf

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from location.models import *
from book.models import *

# Create your views here.

def showmap(request):
	shelfs = range(1,103) # number of shelfs
	cams = range(1,9) # number of cams
	#locations = Location.objects.all()
	#seats = SeatGroup.objects.all()
	context = {
		'shelfs': shelfs,
		'cams' : cams
		#'locations': locations,
		#'seats': seats
	}

	return render(request, 'map.html', context)

	
@csrf_exempt
def setlocation(request):
	arr = [1]
	arr = arr + request.POST['aplist'].split('@')

	X = tf.placeholder("float", [None, 185])
	W = tf.Variable(tf.zeros([185, 75]), name="W")
	hypothesis = tf.nn.softmax(tf.matmul(X, W))
	
	saver = tf.train.Saver({"W":W})
	
	with tf.Session() as sess:
		saver.restore(sess, "/home/ubuntu/bm_web/location/model.ckpt")
		a = sess.run(hypothesis, feed_dict={X:[arr]})
		'''
		[1, -77, -59, -73, -80, -50, -52, -61, -64, -58, -70, -77, -75, -78, -82, -74, -81, -51, -75, -73, -62, -57, -81, -80, -84, -87, -82, -67, -72, -85, -76, -81, -75, -79, -82, -64, -79, -74, -82, -85, -80, -75, -78, -85, -85, -83, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130]
		-77@-59@-73@-80@-50@-52@-61@-64@-58@-70@-77@-75@-78@-82@-74@-81@-51@-75@-73@-62@-57@-81@-80@-84@-87@-82@-67@-72@-85@-76@-81@-75@-79@-82@-64@-79@-74@-82@-85@-80@-75@-78@-85@-85@-83@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130@-130
		'''
		result = sess.run(tf.arg_max(a, 1))
	
	location = Location.objects.get(num = result[0]+1)
	
	var = {'location': location.num, 'top': location.top, 'left': location.left}
	return JsonResponse(var)

@csrf_exempt
def setseat(request):
	seat = Seat.objects.get(num = request.POST['seat'])
	location = request.POST['location']
	seatgroup = seat.seatgroup
	target = seatgroup.location.num
	try:
		if seatgroup.location2 != 0:
			path1 = find_shortest_path(g, location, str(seatgroup.location.num))
			path2 = find_shortest_path(g, location, str(seatgroup.location2))
			target = seatgroup.location2 if len(path1) > len(path2) else seatgroup.location.num
	except:
		None
	
	var = {'seatgroup': seatgroup.num, 'top':seatgroup.top, 'left':seatgroup.left, 'target': target}
	return JsonResponse(var)

@csrf_exempt
def setshelf(request):
	shelf = Bookshelf.objects.get(name = request.POST['shelf'])
	
	var = {'target': shelf.location.num}
	return JsonResponse(var)


@csrf_exempt
def path(request):
	"""
	txt = open('/home/ubuntu/bm_web/location/shelfs.txt', 'r')
	line = txt.readline().splitlines()[0]
	while line:
		
		print "line: " + line
		arr = line.split('-')
		shelfs = arr[1].split(',')
		print arr
		print shelfs
		print shelfs[0]
		for shelf in shelfs:
			shelf1 = shelf + "_1"
			print "shelf1: " + shelf1
			dbshelf = Bookshelf.objects.get(name = shelf1)
			
			dbshelf.location = Location.objects.get(num = arr[0])
			dbshelf.save()
			shelf2 = shelf + "_2"
			dbshelf = Bookshelf.objects.get(name = shelf2)
			dbshelf.location = Location.objects.get(num = arr[0])
			dbshelf.save()
		line = txt.readline().splitlines()[0]
	
	txt = open('/home/ubuntu/bm_web/location/seats.txt', 'r')
	line = txt.readline().splitlines()[0]
	count = 1;
	while line:
		print "line: " + line
		seats = line.split(' ')
		print seats
		sg = SeatGroup.objects.create(num = count)
		sg.save()
		
		for seat in seats:
			print "seat: " + seat
			s = Seat.objects.create(num = int(seat), seatgroup = sg)
			s.save()
		
		count += 1	
		line = txt.readline().splitlines()[0]
	"""
	
	start = request.POST['start']
	end = request.POST['end']
	
	path = find_shortest_path(g, start, end)
	top = []
	left = []
	
	for p in path:
		location = Location.objects.get(num = p)
		top.append(location.top)
		left.append(location.left)
	
	var = {'top': top, 'left': left, 'path': path}
	return JsonResponse(var)

	
g = {   "1" : ["2", "75"],
        "2" : ["1", "3"],
        "3" : ["2", "4"],
        "4" : ["3", "5", "21"],
        "5" : ["4", "6", "21"],
        "6" : ["5", "7"],
        "7" : ["6", "8"],
        "8" : ["7", "9"],
        "9" : ["8", "10"],
        "10" : ["9", "11"],
        "11" : ["10", "12"],
        "12" : ["11", "13"],
        "13" : ["12", "14"],
        "14" : ["13", "15"],
        "15" : ["14", "16"],
        "16" : ["15", "17"],
        "17" : ["16", "18"],
        "18" : ["17", "19", "22"],
        "19" : ["18", "20"],
        "20" : ["19", "21"],
        "21" : ["20", "5"],
        "22" : ["18", "23"],
        "23" : ["22", "24"],
        "24" : ["23", "25"],
        "25" : ["24", "26"],
        "26" : ["25", "27"],
        "27" : ["26", "28"],
        "28" : ["27", "29"],
        "29" : ["28", "30", "32"],
        "30" : ["29", "31"],
        "31" : ["30"],
        "32" : ["29", "33"],
        "33" : ["32", "34"],
        "34" : ["33", "35"],
        "35" : ["34", "36"],
        "36" : ["35", "37"],
        "37" : ["36", "38"],
        "38" : ["37", "39"],
        "39" : ["38", "40"],
        "40" : ["39", "41"],
        "41" : ["40", "42"],
        "42" : ["41", "43"],
        "43" : ["42", "44"],
        "44" : ["43", "45"],
        "45" : ["44", "46", "48"],
        "46" : ["45", "47"],
        "47" : ["46"],
        "48" : ["45", "49"],
        "49" : ["48", "50"],
        "50" : ["49", "51"],
        "51" : ["50", "52"],
        "52" : ["51", "53"],
        "53" : ["52", "54"],
        "54" : ["53", "55"],
        "55" : ["54", "56", "73"],
        "56" : ["55", "57"],
        "57" : ["56", "58"],
        "58" : ["57", "59"],
        "59" : ["58", "60"],
        "60" : ["59", "61"],
        "61" : ["60", "62"],
        "62" : ["61", "63"],
        "63" : ["62", "64", "66"],
        "64" : ["63", "65"],
        "65" : ["64"],
        "66" : ["63", "67"],
        "67" : ["66", "68"],
        "68" : ["67", "69"],
        "69" : ["68", "70", "71"],
        "70" : ["69", "71", "74"],
        "71" : ["69", "70", "72"],
        "72" : ["71", "73"],
        "73" : ["72", "55"],
        "74" : ["70", "75"],
        "75" : ["74", "1"]
    }

def find_shortest_path(graph, start, end, path=[]):
	path = path + [start]
	if start == end:
		return path
	if not graph.has_key(start):
		return None
	shortest = None
	for node in graph[start]:
		if node not in path:
			newpath = find_shortest_path(graph, node, end, path)
			if newpath:
				if not shortest or len(newpath) < len(shortest):
					shortest = newpath
	return shortest
