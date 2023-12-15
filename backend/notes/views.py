from django.utils import timezone
from django.shortcuts import render

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import NoteSerializer, UserSerializer
from .models import Note, User

from .session import Session

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

s = Session()

class LogInView(APIView):
    def post(self, request):
        try:
            username = request.data.get('login')
            password = request.data.get('password')
        except Exception as e:
            return Response({'error': 'Invalid request data format'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(username=username, password=password)
            s.add_user(username)
            print(s.session)
            return Response({'message': 'Logged in', 'session': s.id}, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({'error': 'Wrong credentials'}, status=status.HTTP_401_UNAUTHORIZED)