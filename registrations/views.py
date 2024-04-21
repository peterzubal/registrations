from rest_framework import status, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.hashers import make_password, check_password
from .models import Student
from .serializers import StudentSerializer
from mongoengine import DoesNotExist
import bson

# Custom token model or use a package like djoser
from .tokens import create_token, get_user_from_token, delete_token

class RegisterView(views.APIView):
    def post(self, request, *args, **kwargs):
        mutable_data = request.data.copy()  # Make a mutable copy of the data
        mutable_data['password'] = make_password(mutable_data['password'])
        serializer = StudentSerializer(data=mutable_data)
        if serializer.is_valid():
            user = serializer.save()
            # Handle token creation and return data here...
            return Response({'user_id': user.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        try:
            user = Student.objects.get(username=username)
            if check_password(password, user.password):
                token = create_token(user)
                return Response({'token': token, 'message': "Login successful"}, status=status.HTTP_200_OK)
        except DoesNotExist:
            pass
        return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        delete_token(request.user)
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)

class UpdateProfileView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            student = Student.objects.get(id=bson.ObjectId(request.user.id))
            serializer = StudentSerializer(student, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
        except DoesNotExist:
            pass
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


