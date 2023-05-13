from django.db.models import Q
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from datetime import datetime
import datetime
from django.core.mail import send_mail
from rest_framework.generics import (
    ListAPIView, RetrieveAPIView, CreateAPIView,
    UpdateAPIView, DestroyAPIView, GenericAPIView,
    ListCreateAPIView
)
from .serializers import ( 
    FileSerializer, FileCreateSerializer, AssignAgentSerializer, AllFileSerializer,
    AssignFileAgentSerializer, VeriyDocSerializer, CompleteSerializer,
    ObservationSerializer, ReviewSerializer, DocumentSerializer, LoggerSerializer,
    ActProcedureSerializer, PaymentDocSerializer, PaymentSerializer,
    ResolutionSerializer, ResolutionNotificationSerializer, UnderReviewSerializer,
    NotifiedSerializer, PersonalNotifiedSerializer, FileTypeSerializer, AllTrackSerializer
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from filed.models import File, Agent, Category, VeriyDoc, FileType, LoggerAll
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED,
    HTTP_204_NO_CONTENT
)
from rest_framework.filters import SearchFilter
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from background_task import background

# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)


import schedule
import time

from datetime import timedelta


class FileNumView(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        # query last value of file unique number
        get_file = File.objects.all()
        if get_file.exists():
            print("Has Data")
            # last_file = File.objects.filter(organisation=2).order_by('-id')[0]
            last_file = File.objects.all().order_by('-id')[0]
            file_num = int(last_file.file_name) + 1
            d = "%05d" % ( file_num, )
            print(d)
        else:
            print("Empty")
            file_num = 1
            d = "%05d" % ( file_num, )
            print(d)

        return Response(d)
    
class ResolutionNumView(APIView):

    def get(self, request, format=None):

        last_file = File.objects.all().order_by('-id')[0]
        if last_file.resolution_number is not None:
            file_num = int(last_file.resolution_number[3:]) + 1
            result = "OOT%05d" % ( file_num, )
            print(result)
        else:
            print('variable stores a None value')
            file_num = 1
            result = "OOT%05d" % ( file_num, )
            print(result)

        return Response(result)

class FileSearchView(ListAPIView):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    filter_backends = [SearchFilter]
    search_fields = ['=file_name']

class AllFileView(APIView):
    def get(self, request, format=None):
        logger.warning('Homepage was accessed at '+str(datetime.datetime.now())+' hours!')

        allFiles = File.objects.all()
        serializerAllFile = AllFileSerializer(allFiles, many=True)
        return Response(serializerAllFile.data)
    
class LoggerView(APIView):
    def get(self, request, format=None):
        newDate = datetime.date.today() + datetime.timedelta(days=4)
        print("newDate", newDate)

        loggerFiles = LoggerAll.objects.all()
        serializerAllFile = LoggerSerializer(loggerFiles, many=True)
        return Response(serializerAllFile.data)


class FileListView(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        # allFiles = File.objects.all()
        unassigned_files = File.objects.filter(agent__isnull=True)

        user = self.request.user
        # queryset = File.objects.filter(agent__isnull=False)
        if user.is_organisor:
            queryset = File.objects.filter(agent__isnull=False)
        else:
            queryset = File.objects.filter(agent__isnull=False)
            queryset = queryset.filter(agent__user=user)

        # serializerAllFile = FileSerializer(allFiles, many=True)
        serializerFile = FileSerializer(queryset, many=True)
        unassignedFile = FileSerializer(unassigned_files, many=True)


        # query last value of file unique number
        get_file = File.objects.all()
        if get_file.exists():
            print("Has Data")
            # last_file = File.objects.filter(organisation=2).order_by('-id')[0]
            last_file = File.objects.all().order_by('-id')[0]
            file_num = int(last_file.file_name) + 1
            d = "%05d" % ( file_num, )
            print(d)
        else:
            print("Empty")
            file_num = 1
            d = "%05d" % ( file_num, )
            print(d)

        if user.is_organisor or user.is_support:
            x_id = user.userprofile.id
        else:
            x_id = ""
        
        print("x_id", x_id)

        return Response({
            "user_id": user.id,
            "user_profile": x_id,
            "fileNum": d,
            # "all_files": serializerAllFile.data,
            "files": serializerFile.data,
            "unassigned_files": unassignedFile.data
        })

    def post(self, request, format=None):
        serializer = FileCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            LoggerAll.objects.create(msg='Se creó un nuevo archivo')
            return Response(serializer.data, status= HTTP_201_CREATED)
        return Response(serializer.errors, status= HTTP_400_BAD_REQUEST)

class FileNumSearchView(APIView):
    """
    Retrieve a snippet instance.
    """
    def get_object(self, pk):
        try:
            return File.objects.get(file_name = pk)
        except File.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        filed = self.get_object(pk)
        serializer = FileSerializer(filed)
        Trackserializer = AllTrackSerializer(filed)

        return Response({
            "files" : serializer.data,
            "filesTrack" : Trackserializer.data
            })


class FileDetailView(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return File.objects.get(id=pk)
        except File.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        filed = self.get_object(pk)
        print(filed.id)

        verifyy = VeriyDoc.objects.filter(filev = filed.id)
        # verifySerializer = VeriyDocSerializer(verifyy)
        if verifyy.exists():
            print("Has data")
            verifyy = VeriyDoc.objects.get(filev = filed.id)
            verifySerializer1 = VeriyDocSerializer(verifyy)
            verifySerializer = verifySerializer1.data
        else:
            print("No Data")
            verifySerializer = None

        serializer = FileSerializer(filed)
        return Response({
            "status": "success",
            "files" : serializer.data,
            "verify" : verifySerializer
            })

    def put(self, request, pk, format=None):
        filed = self.get_object(pk)
        serializer = FileCreateSerializer(filed, data=request.data)
        if serializer.is_valid():
            serializer.save()

            LoggerAll.objects.create(msg='Se actualizó un archivo con el número ' + request.data["file_name"])

            # print("ffff data", request.data['State_type'])
            if request.data['State_type'] == 1:
                print("Activo")

                # ====== send email notification ===== #
                email = request.data['email']
                subject= 'seguimiento del estado'
                from_email= settings.EMAIL_HOST_USER
                html_template = 'account/active_file_email.html'
                
                html_message = render_to_string(html_template, {
                    'radicado' : filed.file_name
                })

                message = EmailMessage(subject, html_message, from_email, [email])
                message.content_subtype = 'html' # this is required because there is no plain text email version
                message.send()
            return Response(serializer.data)
        return Response(serializer.errors, status= HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        filed = self.get_object(pk)
        filed.delete()
        return Response(status= HTTP_204_NO_CONTENT)

class FileDetailViewII(RetrieveAPIView):
    def get_object(self, pk):
        try:
            return File.objects.get(id=pk)
        except File.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        filed = self.get_object(pk)
        print(filed.id)

        serializer = FileSerializer(filed)
        return Response(serializer.data)

class TrackDetailView(RetrieveAPIView):
    permission_classes = (AllowAny,)
    serializer_class = AllTrackSerializer
    queryset = File.objects.all()

class verifyDocCreateView(CreateAPIView):
    permission_classes = (AllowAny,)
    # permission_classes = (IsAuthenticated, )
    serializer_class = VeriyDocSerializer
    queryset = VeriyDoc.objects.all()

class verifyDocUpdateView(UpdateAPIView):
    permission_classes = (AllowAny,)
    # permission_classes = (IsAuthenticated, )
    serializer_class = VeriyDocSerializer
    queryset = VeriyDoc.objects.all()

class CompletedStatus(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return File.objects.get(id=pk)
        except File.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        filed = self.get_object(pk)
        
        serializer = CompleteSerializer(filed)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        filed = self.get_object(pk)
        serializer = CompleteSerializer(filed, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status= HTTP_400_BAD_REQUEST)

class AssignAgentRetrieveView(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        user = self.request.user
        queryset = Agent.objects.all()
        allAgent = AssignAgentSerializer(queryset, many=True)

        return Response( allAgent.data)

class AssignAgentView(APIView):
    def get_object(self, pk):
        try:
            return File.objects.get(id=pk)
        except File.DoesNotExist:
            raise Http404
        
    def put(self, request, pk, format=None):
        # User = get_user_model()
        filed = self.get_object(pk)
        serializer = AssignFileAgentSerializer(filed, data=request.data)
        if serializer.is_valid():
            print("filed Data", request.data)
            serializer.save()
            u = Agent.objects.get(id = request.data["agent"])
            # print("u", u.user.email)
            
            LoggerAll.objects.create(msg='Se ha asignado un archivo con este número '+ filed.file_name )

            # ====== send email notification ===== #
            email = u.user.email
            subject= 'Se le ha asignado un tramite'
            from_email= settings.EMAIL_HOST_USER
            html_template = 'account/assign_agent_email.html'
            
            html_message = render_to_string(html_template, {
                'radicado' : filed.file_name
            })

            message = EmailMessage(subject, html_message, from_email, [email])
            message.content_subtype = 'html' # this is required because there is no plain text email version
            message.send()

            return Response(serializer.data)
        return Response(serializer.errors, status= HTTP_400_BAD_REQUEST)

class verifyDocDeleteView(DestroyAPIView):
    permission_classes = (AllowAny, )
    queryset = VeriyDoc.objects.all()

class FileTypeView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = FileTypeSerializer
    queryset = FileType.objects.all()

class UnderReview(UpdateAPIView):
    permission_classes = (AllowAny, )
    serializer_class = UnderReviewSerializer
    queryset = File.objects.all()

class ReviewView(UpdateAPIView):
    permission_classes = (AllowAny, )
    serializer_class = ReviewSerializer
    queryset = File.objects.all()

class ObservationView(APIView):
    def get_object(self, pk):
        try:
            return File.objects.get(id=pk)
        except File.DoesNotExist:
            raise Http404
        
    def put(self, request, pk, format=None):
        filed = self.get_object(pk)
        serializer = ObservationSerializer(filed, data=request.data)
        if serializer.is_valid():
            serializer.save()

            # ====== send email notification ===== #
            email = filed.email
            subject= 'Se ha creado una observación.'
            from_email= settings.EMAIL_HOST_USER
            html_template = 'account/aobserve_email.html'
            
            html_message = render_to_string(html_template, {
                'radicado' : filed.file_name
            })

            message = EmailMessage(subject, html_message, from_email, [email])
            message.content_subtype = 'html' # this is required because there is no plain text email version
            message.send()
            

            return Response(serializer.data)
        return Response(serializer.errors, status= HTTP_400_BAD_REQUEST)


class NotifiedView(UpdateAPIView):
    permission_classes = (AllowAny, )
    serializer_class = NotifiedSerializer
    queryset = File.objects.all()

class DocumentView(UpdateAPIView):
    permission_classes = (AllowAny, )
    serializer_class = DocumentSerializer
    queryset = File.objects.all()

class ActProcedureView(APIView):
    def get_object(self, pk):
        try:
            return File.objects.get(id=pk)
        except File.DoesNotExist:
            raise Http404
        
    def put(self, request, pk, format=None):
        # User = get_user_model()
        filed = self.get_object(pk)
        serializer = ActProcedureSerializer(filed, data=request.data)
        if serializer.is_valid():
            # print("filed Data", filed.email)
            serializer.save()

            # ============================= send email =====================================
            email = filed.email
            subject= 'Se ha creado una Ley de Procedimiento'
            from_email= settings.EMAIL_HOST_USER
            html_template = 'account/act_procedure_email.html'
            
            html_message = render_to_string(html_template, {
                'radicado' : filed.file_name,
                'liquidation_value': filed.liquidation_value
            })

            message = EmailMessage(subject, html_message, from_email, [email])
            message.content_subtype = 'html' # this is required because there is no plain text email version
            message.send()


            return Response(serializer.data)
        return Response(serializer.errors, status= HTTP_400_BAD_REQUEST)

class PersonalNotifiedView(UpdateAPIView):
    permission_classes = (AllowAny, )
    serializer_class = PersonalNotifiedSerializer
    queryset = File.objects.all()

class PaymentView(UpdateAPIView):
    permission_classes = (AllowAny, )
    serializer_class = PaymentSerializer
    queryset = File.objects.all()

class PaymentDocView(UpdateAPIView):
    permission_classes = (AllowAny, )
    serializer_class = PaymentDocSerializer
    queryset = File.objects.all()

class ResolutionView(APIView):
    def get_object(self, pk):
        try:
            return File.objects.get(id=pk)
        except File.DoesNotExist:
            raise Http404
        
    def put(self, request, pk, format=None):
        # User = get_user_model()
        filed = self.get_object(pk)
        serializer = ResolutionSerializer(filed, data=request.data)
        if serializer.is_valid():
            # print("filed Data", filed.email)
            serializer.save()

            # ============================= send email =====================================
            email = filed.email
            subject= 'Se genero tu resolusión'
            from_email= settings.EMAIL_HOST_USER
            html_template = 'account/aresolution_email.html'
            
            html_message = render_to_string(html_template, {
                'radicado' : filed.file_name
            })

            message = EmailMessage(subject, html_message, from_email, [email])
            message.content_subtype = 'html' # this is required because there is no plain text email version
            message.send()


            return Response(serializer.data)
        return Response(serializer.errors, status= HTTP_400_BAD_REQUEST)

class ResolutionNotificationView(UpdateAPIView):
    permission_classes = (AllowAny, )
    serializer_class = ResolutionNotificationSerializer
    queryset = File.objects.all()


