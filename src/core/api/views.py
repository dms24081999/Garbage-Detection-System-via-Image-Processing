from django.contrib.auth import get_user_model
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
from django.db.models.functions import Concat
from django.db.models import Value
from .serializers import (
    UserSerializer,
    GarbageDataSerializer
)
from ..models import GarbageDataModel
from rest_framework.generics import (
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
)
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_201_CREATED
)
from rest_framework.views import APIView
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated
)
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from allauth.account.models import EmailConfirmation, EmailConfirmationHMAC
from django.http import HttpResponse, HttpResponseRedirect
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from rest_auth.registration.views import SocialLoginView
from rest_auth.registration.views import SocialConnectView
# from posts.api.serializers import PostDetailSerializer
# from posts.api.pagination import StandardResultPagination
# from posts.models import Post
from django.utils import timezone
from django.contrib.sessions.models import Session
import datetime


User=get_user_model()


class GoogleLogin(SocialConnectView):
    adapter_class = GoogleOAuth2Adapter


class ConfirmEmailView(APIView):
    permission_classes = [AllowAny]

    def get(self, *args, **kwargs):
        self.object = confirmation = self.get_object()
        try:
            confirmation.confirm(self.request)
            return Response({"details":"E-mail ID registered successfully!"})
        except:
        # A React Router Route will handle the failure scenario
            return Response({"details":"Failed to register E-mail ID. Invalid Link!"})

    def get_object(self, queryset=None):
        key = self.kwargs['key']
        email_confirmation = EmailConfirmationHMAC.from_key(key)
        if not email_confirmation:
            if queryset is None:
                queryset = self.get_queryset()
            try:
                email_confirmation = queryset.get(key=key.lower())
            except EmailConfirmation.DoesNotExist:
                # A React Router Route will handle the failure scenario
                return Response({"details":"Failed to register E-mail ID. An error occured!"})
        return email_confirmation

    def get_queryset(self):
        qs = EmailConfirmation.objects.all_valid()
        qs = qs.select_related("email_address__user")
        return qs

    
class DeleteAllUnexpiredSessionsForUser(APIView):
    def get(self, request):
        try:
            unexpired_sessions = Session.objects.filter(expire_date__gte=timezone.now())
            for session in unexpired_sessions:
                print(session.session_key)
            print(request.session.session_key)    
            [
                session.delete() for session in unexpired_sessions if str(session.session_key)!=str(request.session.session_key)
                if str(request.user.id) == session.get_decoded().get('_auth_user_id')
            ] 
        except:
            return Response({"detail":"Error!"})
        return Response({"detail":"Successfully deleted all existing sessions!"})


class CurrentUserAPIView(APIView):
    def get(self, request):
        serializer = UserSerializer(request.user,context={'request': request})
        newdict={"sessionkey":request.session.session_key}
        newdict.update(serializer.data)
        return Response(serializer.data)


class UserView(ModelViewSet):
    lookup_field= 'pk'
    serializer_class=UserSerializer
    permission_classes = [AllowAny]
    queryset =User.objects.all()

    

    def get_queryset(self, *args, **kwargs):
        queryset = super(UserView, self).get_queryset(*args, **kwargs)
        qs=User.objects.all()
        query=self.request.GET.get('s')
        if query is not None:
            qs=qs.filter(
                Q(username__icontains=query)|
                Q(first_name__icontains=query)|
                Q(last_name__icontains=query)
            ).distinct()
        return qs
    
    def retrieve(self, request, pk, *args, **kwargs):
        print("current pk",pk,request.user.pk)
        if not request.user.is_authenticated:
            return Response({"detail": "Auth not provided."}, status=400)
        # elif int(pk)!=int(request.user.pk):
        #     return Response({"detail": "Not found."}, status=400)
        else:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
            
    def update(self, request, pk, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"detail": "Auth not provided."}, status=400)
        elif int(pk)!=int(request.user.pk):
            return Response({"detail": "Not found."}, status=400)
        else:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)

    def destroy(self, request, pk, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"detail": "Auth not provided."}, status=400)
        elif int(pk)!=int(request.user.pk):
            return Response({"detail": "Not found."}, status=400)
        else:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)



class GarbageDataView(ModelViewSet):
    lookup_field= 'pk'
    serializer_class=GarbageDataSerializer
    permission_classes = [AllowAny]
    queryset =GarbageDataModel.objects.all()

    # def create(self, request, *args, **kwargs):
        
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     print(serializer.data["photo"])
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self, *args, **kwargs):
        queryset = super(GarbageDataView, self).get_queryset(*args, **kwargs)
        qs=GarbageDataModel.objects.all()
        # query=self.request.GET.get('s')
        # if query is not None:
        #     qs=qs.filter(
        #         Q(username__icontains=query)|
        #         Q(first_name__icontains=query)|
        #         Q(last_name__icontains=query)
        #     ).distinct()
        return qs
    
    def retrieve(self, request, pk, *args, **kwargs):
        print("current pk",pk,request.user.pk)
        if not request.user.is_authenticated:
            return Response({"detail": "Auth not provided."}, status=400)
        else:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
            
    def update(self, request, pk, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"detail": "Auth not provided."}, status=400)
        # elif int(pk)!=int(request.user.pk):
        #     return Response({"detail": "Not found."}, status=400)
        else:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)

    def destroy(self, request, pk, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"detail": "Auth not provided."}, status=400)
        # elif int(pk)!=int(request.user.pk):
        #     return Response({"detail": "Not found."}, status=400)
        else:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)

