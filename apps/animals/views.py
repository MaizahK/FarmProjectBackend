import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import AnimalAssetSerializer

class AnimalGateWayView(APIView):
    FARMOS_URL = "http://localhost:8081/api/asset/animal/"
    HEADERS = {
        "Content-Type": "application/vnd.api+json",
        "Accept": "application/vnd.api+json",
        # "Authorization": "Bearer <your_token>" 
    }

    def get(self, request, pk=None):
        """List animals or retrieve one."""
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return Response({"message": "Authorization header missing"}, status=status.HTTP_401_UNAUTHORIZED)
        self.HEADERS.update({"Authorization": auth_header})
        url = f"{self.FARMOS_URL}/{pk}" if pk else self.FARMOS_URL
        print(url)
        response = requests.get(url, headers=self.HEADERS)

        print(response.text)
        
        if response.status_code == 200:
            data = response.json().get('data')
            serializer = AnimalAssetSerializer(data, many=not pk)
            return Response(serializer.data)
        return Response({"message" : response.text}, status=response.status_code)

    def post(self, request):
        """Create an animal."""
        serializer = AnimalAssetSerializer(data=request.data)
        if serializer.is_valid():
            # serializer.validated_data now contains the farmOS-ready nested dict
            response = requests.post(
                self.FARMOS_URL, 
                json=serializer.validated_data, 
                headers=self.HEADERS
            )
            if response.status_code == 201:
                return Response(
                    AnimalAssetSerializer(response.json()['data']).data, 
                    status=status.HTTP_201_CREATED
                )
            return Response(response.json(), status=response.status_code)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        """Update an animal."""
        # farmOS requires the ID in the data body for PATCH
        serializer = AnimalAssetSerializer(data=request.data)
        if serializer.is_valid():
            payload = serializer.validated_data
            payload['data']['id'] = pk  # Inject the ID for JSON:API compliance
            
            response = requests.patch(
                f"{self.FARMOS_URL}/{pk}", 
                json=payload, 
                headers=self.HEADERS
            )
            return Response(response.json(), status=response.status_code)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """Delete an animal."""
        response = requests.delete(f"{self.FARMOS_URL}/{pk}", headers=self.HEADERS)
        if response.status_code == 204:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(response.json(), status=response.status_code)