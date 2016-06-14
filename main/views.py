from django.shortcuts import render
from book.models import *
from main.models import *
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
# Create your views here.


import datetime as dt
from datetime import datetime

def index(request):
	dList = []
	
	for i in range(0,10) :
		date = dt.date.today() - dt.timedelta(days = 9) + dt.timedelta(days = i)
		if not (Book_AddDate.objects.filter(date = date).exists()) :
			b_adate = Book_AddDate(date = date, count = 0)
			b_adate.save()
		else :
			b_adate = Book_AddDate.objects.get(date = date)
		
		if not (Book_SearchDate.objects.filter(date = date ).exists()) :
			b_sdate = Book_SearchDate(date = date, count = 0) 
			b_sdate.save()
		else :
			b_sdate = Book_SearchDate.objects.get(date = date)
			
		dList.append({'date': date.isoformat() , 'b_adate': b_adate.count, 'b_sdate': b_sdate.count})
		
	dt.date.today() + dt.timedelta(days = 1)
	comCount = Comments.objects.filter(time__date = dt.date.today() ).count();
	context = {
		'dList': dList,
		'item': dList[9], # latest
		'comment': comCount
	}
	
	
	return render(request, 'main/index.html', context)
	

def shelfs(request):
	shelfs = Bookshelf.objects.all()
	context ={'shelfs':shelfs}

	return render(request, 'main/shelfs.html', context)


def books(request):
	books = Book.objects.all()
	context ={'books':books}
	
	return render(request, 'main/books.html', context)
	
def comments(request):
	comments = Comments.objects.all().order_by('-time')
	context ={'comments': comments}
	
	return render(request, 'main/comments.html', context)
	

@csrf_exempt
def addcomment(request):
	content = request.POST['content']
	comment = Comments(content = content, time = datetime.now())
	comment.save()
	var = {'content': comment.content , 'time': comment.time}
	return JsonResponse(var)
	
def addbooks(request):

	return render(request, 'main/addbooks.html')