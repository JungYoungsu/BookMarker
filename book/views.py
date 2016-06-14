# -*- coding: utf-8 -*- 

from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.template import loader
from django.core.files.uploadedfile import InMemoryUploadedFile

from bs4 import BeautifulSoup
from openpyxl import load_workbook
from base64 import b64decode
from PIL import Image
from io import BytesIO


from book.models import *
from main.models import *

import json
import urllib
import os.path
import datetime
import base64
import StringIO


	
def readXLS(request):
	BASE = os.path.dirname(os.path.abspath(__file__))
	wb = load_workbook(filename=os.path.join(BASE, "test1.xlsx"), read_only=True)
	ws = wb['Sheet1']
	
	for row in ws.rows:
		if row[0].value is not None:
			if row[1].value is None:
				break;
			try:
				lower_mark = row[1].value.split('~')[0].strip().encode('utf-8')
				upper_mark = row[1].value.split('~')[1].strip().encode('utf-8')
				name = str(row[0].value)+"_1"
				
				shelf1 = Bookshelf(name = name, lower_mark = lower_mark, upper_mark = upper_mark)
				shelf1.save()

				lower_mark = row[2].value.split('~')[0].strip().encode('utf-8')
				upper_mark = row[2].value.split('~')[1].strip().encode('utf-8')  # 양쪽 연속 공백 지우기
				name = str(row[0].value)+"_2"
				
				shelf2 = Bookshelf(name = name, lower_mark = lower_mark, upper_mark = upper_mark)
				shelf2.save()
			except Exception as e:
				print "Error : " + str(e)
	

def parseBook(cid):
	html = urllib.urlopen('http://library.cau.ac.kr/search/DetailView.ax?cid='+str(cid))
	soup = BeautifulSoup(html, 'html.parser')
	body = soup.find(id="metaDataBody")

	typeTag = body.find("td", string="자료유형 :")
	type = typeTag.next_sibling.next_sibling.string.strip() # 양쪽 연속 공백 지우기
	 
	title_authorTag = body.find("td", string="서명 / 저자 : ")
	title_authorTag = title_authorTag.next_sibling.string
	title = title_authorTag.split('/')[0].strip() # 양쪽 연속 공백 지우기
	author = title_authorTag.split('/')[1].strip() # 양쪽 연속 공백 지우기
	
	markTag = body.find("td", string="청구기호 : ")
	mark = markTag.next_sibling.string.strip() # 양쪽 연속 공백 지우기
	
	createBook(cid,type,title,author,mark)

	
def createBook(cid,type,title,author,mark):
	shelfs = Bookshelf.objects.all()
	marktemp = mark.split(' ')
	
	for shelf in shelfs:
		result = False
		lower_mark = shelf.lower_mark.split(' ')
		if lower_mark[0].count('.') and marktemp[0].count('.'): # 둘다 맨앞 숫자가 . 으로 나눠져 있는 경우
			if not lower_mark[0].split('.')[0] <= marktemp[0].split('.')[0] :
				continue
			if lower_mark[0].split('.')[0] == marktemp[0].split('.')[0] :	# 맨앞 숫자가 같은 경우 두번째 숫자 비교
				if not lower_mark[0].split('.')[1] <= marktemp[0].split('.')[1] :
					continue
				if lower_mark[0].split('.')[1] == marktemp[0].split('.')[1] : # 두번째 숫자도 같으면 나머지 비교
					if not lower_mark[1] <= marktemp[1] :
						continue
				
		elif not lower_mark[0].count('.') and marktemp[0].count('.'): # mark만 . 으로 나눠져 있는 경우
			if not lower_mark[0] <= marktemp[0].split('.')[0] :
				continue
				
		elif lower_mark[0].count('.') and not marktemp[0].count('.'): # lower만 . 으로 나눠져 있는 경우
			if not lower_mark[0].split('.')[0] <= marktemp[0] :
				continue
			if lower_mark[0].split('.')[0] == marktemp[0] : # 앞 숫자가 같은 경우  ex) 951.1 < 951 => False
				continue
				
		else : # 둘 다 . 으로 안 나눠져 있는 경우
			if not lower_mark[0] <= marktemp[0] :
				continue
			if lower_mark[0] == marktemp[0] :
				if not lower_mark[1] <= marktemp[1] :
					continue
		
		
		
		upper_mark = shelf.upper_mark.split(' ')
		
		if marktemp[0].count('.') and upper_mark[0].count('.'): # 둘다 맨앞 숫자가 . 으로 나눠져 있는 경우
			if not marktemp[0].split('.')[0] <= upper_mark[0].split('.')[0]  :
				continue
			if upper_mark[0].split('.')[0] == marktemp[0].split('.')[0] :	# 맨앞 숫자가 같은 경우 두번째 숫자 비교
				if not marktemp[0].split('.')[1] <= upper_mark[0].split('.')[1]:
					continue
				if marktemp[0].split('.')[1] == upper_mark[0].split('.')[1]  : # 두번째 숫자도 같으면 나머지 비교
					if not marktemp[1] <= upper_mark[1] :
						continue
				
		elif marktemp[0].count('.') and not upper_mark[0].count('.'): # mark만 . 으로 나눠져 있는 경우
			if not marktemp[0].split('.')[0] <= upper_mark[0] :
				continue
			if marktemp[0].split('.')[0] == upper_mark[0] :	# 앞 숫자가 같은 경우  ex) 951.1 < 951 => False
				continue
				
		elif not marktemp[0].count('.') and upper_mark[0].count('.') : # upper만 . 으로 나눠져 있는 경우
			if not marktemp[0] <=  upper_mark[0].split('.')[0] :
				continue
				
		else : # 둘 다 . 으로 안 나눠져 있는 경우
			if not marktemp[0] <= upper_mark[0] :
				continue
			if marktemp[0] == upper_mark[0] :
				if not marktemp[1] <= upper_mark[1] :
					continue
		
		bookshelf = shelf
		break
	
	
	book = Book(cid = cid, type = type, title = title, author = author, mark = mark, bookshelf = bookshelf)
	book.save()
	
	if not (Book_AddDate.objects.filter(date = datetime.date.today()).exists()) :
		date = Book_AddDate(date = datetime.date.today(), count = 1)
	else :
		date = Book_AddDate.objects.get(date = datetime.date.today())
		date.count = date.count + 1
	date.save()
	return True

@csrf_exempt	
def addSideimg(request):
	try:
		cid = request.POST['cid']
		img = request.POST['img']
		img = img.replace("data:image/jpeg;base64,", "")
	except:
		variables = {'success': False, 'reason': "Request- POST [cid, img] is null"}
		return HttpResponse(json.dumps(variables), content_type='application/json')
	
	try:
		if not Book.objects.filter(cid = cid).exists():
			parseBook(cid)
			
		book = Book.objects.get(cid = cid)
	except Exception as e:
		variables = {'success': False, 'reason': "Book object :: " + str (e)}
		return HttpResponse(json.dumps(variables), content_type='application/json')

	try:
		filename = cid + ".jpg"
		tempfile = Image.open(BytesIO(b64decode(img)))
		tempfile_io = StringIO.StringIO()
		print "ee3"
		tempfile.save(tempfile_io, format='JPEG')
		print "ee2"
		image_file = InMemoryUploadedFile(tempfile_io, None, filename,'image/jpeg',tempfile_io.len, None)
		print "ee"
		book.sideImage.save(filename, image_file, save=True)
	except Exception as e:
		variables = {'success': False, 'reason': "Save img fail :: " + str (e)}
		return HttpResponse(json.dumps(variables), content_type='application/json')
	
	variables = {'success': True, 'reason': ""}
	return HttpResponse(json.dumps(variables), content_type='application/json')
	
	
	
@csrf_exempt
def getBook(request):
	try:
		cid = request.POST['cid']
	except:
		cid = ""
	try:
		mark = request.POST['mark']
	except:
		mark = ""
		
	if mark == "" and cid == "" :
		variables = {'success': False, 'reason': "Request- POST [cid, mark] is null"}
		return HttpResponse(json.dumps(variables), content_type='application/json')
	
	if mark == "":
		try:
			if not Book.objects.filter(cid = cid).exists():
				parseBook(cid)
				
			book = Book.objects.get(cid = cid)
		except Exception as e:
			variables = {'success': False, 'reason': "Book object :: " + str (e)}
			return HttpResponse(json.dumps(variables), content_type='application/json')
	else:
		try:
			if not Book.objects.filter(mark = mark).exists():
				variables = {'success': False, 'reason': mark + " : Book does not exist in Server" }
				return HttpResponse(json.dumps(variables), content_type='application/json')
			book = Book.objects.get(mark = mark)
		except Exception as e:
			variables = {'success': False, 'reason': "Book object :: " + str (e)}
			return HttpResponse(json.dumps(variables), content_type='application/json')
	
	
	
	
	if not (Book_SearchDate.objects.filter(date = datetime.date.today()).exists()) :
		date = Book_SearchDate(date = datetime.date.today(), count = 1) 
	else :
		date = Book_SearchDate.objects.get(date = datetime.date.today())
		date.count = date.count + 1
	date.save()
	
	feature = ""
	if not book.sideImage == '' :
		feature = book.sideImage.url
	
	variables = {'success': True, 'title': book.title, 'author': book.author, 'mark': book.mark, 
		'feature': feature, 'bookshelf':book.bookshelf.name}
	return HttpResponse(json.dumps(variables), content_type='application/json')