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
import os 
import pwd
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
	filenam = "/home/sumitrathore1313/apps/django/django_projects/Project/ResumeParser/ResumeTransducer/data/"+filename
        #return Response({'data': pwd.getpwuid( os.getuid() )[ 0 ]})
	with open(filenam, 'wb+') as temp_file:
            for chunk in my_file.chunks():
                temp_file.write(chunk)
        #return Response({'data': "hello"})
	input_file = filename
        output_file = filename.split('.')[0]
        cmd = "java -cp 'bin/*:../GATEFiles/lib/*:../GATEFiles/bin/gate.jar:lib/*' code4goal.antony.resumeparser.ResumeParserProgram data/%s data/%s.json" % (input_file, output_file)
	#cmd = "java -cp 'ResumeParser/ResumeTransducer/bin/*:ResumeParser/GATEFiles/lib/*:ResumeParser/GATEFiles/bin/gate.jar:ResumeParser/ResumeTransducer/lib/*' code4goal.antony.resumeparser.ResumeParserProgram %s %s.json" % (input_file, output_file)
        os.chdir("/home/sumitrathore1313/apps/django/django_projects/Project/ResumeParser/ResumeTransducer/")
	out = subprocess.check_output(cmd, shell=True)
        #return Response({'data': out})
	with open("/home/sumitrathore1313/apps/django/django_projects/Project/ResumeParser/ResumeTransducer/data/%s.json" % (output_file)) as json_data:
            data = json.load(json_data)
    
        return Response({'data': data})
