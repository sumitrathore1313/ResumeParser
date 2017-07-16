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

        with open(filename, 'wb+') as temp_file:
            for chunk in my_file.chunks():
                temp_file.write(chunk)
        input_file = filename
        output_file = "sample"
        cmd = "java -cp 'ResumeParser/ResumeTransducer/bin/*:ResumeParser/GATEFiles/lib/*:ResumeParser/GATEFiles/bin/gate.jar:ResumeParser/ResumeTransducer/lib/*' code4goal.antony.resumeparser.ResumeParserProgram %s %s.json" % (input_file, output_file)
        subprocess.Popen(cmd, shell=True)
        with open('sample.json') as json_data:
            data = json.load(json_data)
    
        return Response({'data': data})
