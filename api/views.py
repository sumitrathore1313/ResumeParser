# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from rest_framework import generics, views
from .serializers import BucketlistSerializer
from .models import Bucketlist
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
import subprocess
import json
from Helper import pdf2txt
from Helper import GramGloveSentenceVector
import os

class CreateView(generics.ListCreateAPIView):
    """This class defines the create behavior of our rest api."""
    queryset = Bucketlist.objects.all()
    serializer_class = BucketlistSerializer

    def perform_create(self, serializer):
        """Save the post data when creating a new bucketlist."""
        serializer.save()


class DetailsView(generics.RetrieveUpdateDestroyAPIView):
    """This class handles the http GET, PUT and DELETE requests."""

    queryset = Bucketlist.objects.all()
    serializer_class = BucketlistSerializer

class FileUploadView(views.APIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def post(self, request,filename, format=None):
        my_file = request.FILES['file']

        with open('/home/sumitrathore1313/apps/django/django_projects/Project/data/'+filename, 'wb+') as temp_file:
            for chunk in my_file.chunks():
                temp_file.write(chunk)
        input_file = '/home/sumitrathore1313/apps/django/django_projects/Project/data/'+filename
        output_file = '/home/sumitrathore1313/apps/django/django_projects/Project/data/'+filename.split('.')[0]
        cmd = "java -cp 'bin/*:../GATEFiles/lib/*:../GATEFiles/bin/gate.jar:lib/*' code4goal.antony.resumeparser.ResumeParserProgram %s %s.json" % (input_file, output_file)
        os.chdir("/home/sumitrathore1313/apps/django/django_projects/Project/ResumeParser/ResumeTransducer/")
	subprocess.Popen(cmd, shell=True)
        import time
        time.sleep(20)
        with open('/home/sumitrathore1313/apps/django/django_projects/Project/data/'+filename.split('.')[0]+'.json') as json_data:
            data = json.load(json_data)

        return Response({'data': data})

class Registration(views.APIView):
    """docstring for Registration."""

    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def post(self, request,filename ,format=None):

        my_file = request.FILES['file']

        with open('/home/sumitrathore1313/apps/django/django_projects/Project/data/'+filename, 'wb+') as temp_file:
            for chunk in my_file.chunks():
                temp_file.write(chunk)
        input_file = '/home/sumitrathore1313/apps/django/django_projects/Project/data/'+filename
        output_file = '/home/sumitrathore1313/apps/django/django_projects/Project/data/'+filename.split('.')[0]
        cmd = "java -cp 'bin/*:../GATEFiles/lib/*:../GATEFiles/bin/gate.jar:lib/*' code4goal.antony.resumeparser.ResumeParserProgram %s %s.json" % (input_file, output_file)
	#cmd = "java -cp 'ResumeParser/ResumeTransducer/bin/*:ResumeParser/GATEFiles/lib/*:ResumeParser/GATEFiles/bin/gate.jar:ResumeParser/ResumeTransducer/lib/*' code4goal.antony.resumeparser.ResumeParserProgram %s %s.json" % (input_file, output_file)
	os.chdir("/home/sumitrathore1313/apps/django/django_projects/Project/ResumeParser/ResumeTransducer/")
        #subprocess.Popen(cmd, shell=True)
        import time
        time.sleep(2)
        with open('/home/sumitrathore1313/apps/django/django_projects/Project/data/'+filename.split('.')[0]+'.json') as json_data:
            data = json.load(json_data)
	data = data['basics']
	name = []
	email = []
	middlename = ''
	firstName = ''
	surname = ''
	tempname = data['name']
        try:
                middlename = data['name']['middlename']
        except KeyError:
		pass
	try:
                firstName = data['name']['firstName']
	except KeyError:
		pass        
	try:
                surname = data['name']['surname']
	except KeyError:
		pass	
	try:
                for i in range(len(data['email'])):
                        email.append(data['email'][i])
     	except KeyError:
		pass
	name.append(firstName+' '+middlename+' '+surname)
	from keras.models import load_model
	classifier_path = "/home/sumitrathore1313/apps/django/django_projects/Project/data/Test/classifier5"
	filepath = output_file+'.txt'
	pdf2txt.convert(input_file, output_file)
	gsv = GramGloveSentenceVector(filepath,dimension=300, training=False)
	sen2vec = gsv.get_5gram_sentenceVector()
	classifier = load_model(classifier_path)	
	import numpy as np
	y_pred = classifier.predict(np.array(sen2vec))	
	with open(filepath, 'r') as f:
    		content = f.readlines()
	count = 0
	labels = ['basic', 'experience', 'education', 'certificate', 'extra', 'skills', 'projects','summary', 'mimc']
	basic = []
	for line in content:
    		if np.argmax(y_pred, 1)[count] == 0:
        		basic.append(line.strip())
    		count += 1
	
	return Response({'name': name, 'email': basic})
