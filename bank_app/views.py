from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

import pandas as pd

from .utils import process

# Create your views here.

def index(request):
	if "GET" == request.method:
		return render(request, 'bank_app/index.html', {})

	csv_file = request.FILES["csv_file"]
	print('______________\n\n')
	# print(type(csv_file))

	# file_data = csv_file.read().decode("utf-8")

	df = pd.read_csv(csv_file)
	del csv_file
	print('uploaded:')
	print(df.columns)

	try:
		accuracy = process(df)
		print('accuracy: ', accuracy)
		# return HttpResponse('<br>Accuracy is : {}'.format(str(accuracy)))
		return render(request, 'bank_app/index.html', {"acc": str(accuracy)})

	except Exception as e:
		print('\n',e,'\n')
		return render(request, 'bank_app/index.html', {"acc": 'error'})

	
	return render(request, 'bank_app/index.html', {})