from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import LoginSerializer, SignUpSerializer
import requests
from utils.constants import FARMOS_BASE_URL, FARMOS_CLIENT_ID, FARMOS_CLIENT_SECRET


class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            # Call FarmOS login endpoint
            resp = requests.post(f"{FARMOS_BASE_URL}/oauth/token/", data={
                "grant_type": "password",
                "client_id": data.get("username"),
                "client_secret" : FARMOS_CLIENT_SECRET,
                "username" : "user",
                "password" : "farmos_password",
                "scope" : "farm_manager"
            })
            if resp.status_code != 200:
                return Response({"error": "Invalid credentials", "message": resp.text}, status=status.HTTP_401_UNAUTHORIZED)
            
            return Response(resp.json(), status=resp.status_code)
        except requests.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LogoutAPIView(APIView):
    def delete(self, request):
        token = request.headers.get("Authorization")
        if not token:
            return Response({"error": "Authorization header missing"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            resp = requests.post(f"{FARMOS_BASE_URL}/user/logout", headers={"Authorization": token})
            return Response(resp.json(), status=resp.status_code)
        except requests.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SignUpAPIView(APIView):
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            # Call FarmOS user creation endpoint
            resp = requests.post(f"{FARMOS_BASE_URL}/user/register", json={
                "name": data['username'],
                "mail": data['email'],
                "pass": data['password']
            })
            if resp.status_code != 201:
                return Response(resp.json(), status=resp.status_code)
            
            return Response(resp.json(), status=resp.status_code)
        except requests.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
