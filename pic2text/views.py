from django.shortcuts import render
from django.http import HttpResponse
import os
import configparser
from aip import AipOcr
from upload import settings

"""just test for git reset."""

def upload(request):
	return render(request, 'pic2text/upload.html')

def aip_client(work_order):
	target = configparser.ConfigParser()
	target.read(work_order)  
	APP_ID = target.get('pic2text', "AppID")
	API_KEY = target.get('pic2text', "API_Key")
	SECRET_KEY = target.get('pic2text', "Secret_Key")
	client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
	return client

def get_text(client, image):
	result_dict = client.basicAccurate(image)
	text = ''
	words_result = result_dict.get("words_result")
	if words_result:
		for words_dict in words_result:
			text += words_dict.get('words', '') + '\r\n'
		return text

def return_text(request):
	work_order = os.path.join(settings.SOURCE_DIRS, 'baidu/character_recognition.ini')
	client = aip_client(work_order)
	pic = request.FILES.get("pic")
	if not pic:
		error = '未选择文件'
		return HttpResponse(error)
	filename = pic.name
	image = pic.read()
	text = get_text(client, image)
	if not text:
		error = '转换失败'
		return HttpResponse(error)
	context = {'filename':filename, 'text':text}
	return render(request, 'pic2text/result.html', context=context)
