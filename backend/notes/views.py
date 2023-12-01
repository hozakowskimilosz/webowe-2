from django.utils import timezone
from django.shortcuts import render

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import NoteSerializer, UserSerializer
from .models import Note, User
from .sessions import Sessions


class NoteView(generics.ListAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

class UserView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CreateNoteView(APIView):
    def post(self, request):
        note_text = request.data.get('note_text')
        owner_id = request.data.get('owner')  # Assuming owner is an ID
        print(note_text, owner_id)
        try:
            owner = User.objects.get(id=owner_id)
            Note.objects.create(
                note_text=note_text,
                pub_date=timezone.now(),
                owner=owner
            )
            return Response({'message': 'Note created successfully'}, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({'error': 'User not found'})

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class LogInView(APIView):
    def post(self, request):
        username = request.data.get('login')
        password = request.data.get('password')
        userObjects = User.objects.all().values()
        
        correctCredentials = False
        for user in userObjects:
            if user['username'] == username and user['password'] == password:
                correctCredentials = True
        if correctCredentials: 
            s = Sessions(username)
            s.sessionLogin
            return Response({'message': 'Logged in'}, status=status.HTTP_201_CREATED)
        return Response({'error': 'Wrong credentials'})
