import jwt, csv, hashlib
from rest_framework import status

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.conf import settings
from django.http import HttpResponse

from .models import Client, Product, Bill
from .serializers import ClientSerializer, ProductSerializer, BillSerializer, ClientLoginSerializer
from .jwt_authentication import JWTAuthentication




class ClientListView(APIView):
    def get(self, request):
        clients = Client.objects.all()
        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data)
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


class ProductListView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


class BillListView(APIView):
    def get(self, request):
        bills = Bill.objects.all()
        serializer = BillSerializer(bills, many=True)
        return Response(serializer.data)
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]



class UserRegistrationView(APIView):
    def post(self, request):
        hashed_password = hashlib.sha256(request.data['password'].encode()).hexdigest()
        request.data['password'] = hashed_password
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            client = serializer.save()
            token_payload = {'user_id': client.id}
            token = jwt.encode(token_payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
            
            return Response({'message': 'Cliente registrado exitosamente', 'token': token}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):

    def post(self, request):
        serializer = ClientLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')

        try:
            # Buscamos al usuario por correo electrónico
            client = Client.objects.get(email=email)
        except Client.DoesNotExist:
            return Response({'message': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)

        # Verificamos la contraseña
        if client.password == hashlib.sha256(password.encode()).hexdigest():
            # Si las credenciales son válidas, generamos tokens de acceso y actualización
            token_payload = {'user_id': client.id}
            token = jwt.encode(token_payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


            return Response({'message': 'Inicio de sesión exitoso', 'token': token}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)
                







@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def download_clients_csv(request):
    #print(JWTAuthentication().authenticate(request))
    #if JWTAuthentication().authenticate(request) == False:
        #return JsonResponse({'error': 'No tienes autorización para realizar esta operación'}, status=401)
    
    if request.method == 'GET':
        clients = Client.objects.all()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="clients.csv"'
        csv_writer = csv.writer(response)
        csv_writer.writerow(['document', 'first_name', 'last_name', 'email', 'password'])
        for client in clients:
            csv_writer.writerow([client.document, client.first_name, client.last_name, client.email, client.password])

        return response

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def upload_clients_csv(request):
    if request.method == 'POST':
        if 'csv_file' not in request.FILES:
            return JsonResponse({'error': 'No se proporcionó ningún archivo CSV'}, status=400)

        csv_file = request.FILES['csv_file']
        try:
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)
            for row in reader:
                client = Client.objects.create(
                    document=row['document'],
                    first_name=row['first_name'],
                    last_name=row['last_name'],
                    email=row['email'],
                    password=row['password']
                )

            return JsonResponse({'message': 'Datos del CSV cargados exitosamente'}, status=200)

        except Exception as e:
            return JsonResponse({'error': f'Error al procesar el archivo CSV: {str(e)}'}, status=500)