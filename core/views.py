import jwt, csv, hashlib
from rest_framework import status

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.conf import settings
from django.http import HttpResponse
from django.db import connection

from .models import Client, Product, Bill
from .serializers import ClientSerializer, ProductSerializer, BillSerializer, ClientLoginSerializer
from .jwt_authentication import JWTAuthentication



class ClientOneView(APIView):
    def get(self, request, pk):
        client = Client.objects.get(pk=pk)
        serializer = ClientSerializer(client)
        return Response(serializer.data)
    
    def put(self, request, pk):
        client = Client.objects.get(pk=pk)
        if request.data['password']:
            hashed_password = hashlib.sha256(request.data['password'].encode()).hexdigest()
            request.data['password'] = hashed_password
        serializer = ClientSerializer(client, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


class ClientListView(APIView):
    def get(self, request):
        #clients = Client.objects.all()
        #serializer = ClientSerializer(clients, many=True)
        #return Response(serializer.data)
        query = "SELECT * FROM core_client"
        raw_queryset = Client.objects.raw(query)
        results = [{'document': obj.document, 'email': obj.email, 'first_name': obj.first_name, 'last_name': obj.last_name} for obj in raw_queryset]
        return JsonResponse({'results': results})
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]




class ProductOneView(APIView):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    
    def put(self, request, pk):
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

class ProductListView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]



class BillOneView(APIView):
    def get(self, request, pk):
        bill = Bill.objects.get(pk=pk)
        serializer = BillSerializer(bill)
        return Response(serializer.data)
    
    def put(self, request, pk):
        bill = Bill.objects.get(pk=pk)
        serializer = BillSerializer(bill, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

class BillListView(APIView):
    def get(self, request):
        query = "SELECT * FROM core_bill"
        raw_queryset = Bill.objects.raw(query)
        results = [{'client_id': obj.client_id, 'company_name': obj.company_name, 'nit': obj.nit, 'code': obj.code} for obj in raw_queryset]
        return JsonResponse({'results': results})
    
    def post(self, request):
        #serializer = BillSerializer(data=request.data)
        #if serializer.is_valid():
            #serializer.save()
            #return Response(serializer.data, status=status.HTTP_201_CREATED)
        #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        query = "INSERT INTO core_bill (client_id, company_name, nit, code) VALUES (%s, %s, %s, %s)"
        values = (request.data['client_id'], request.data['company_name'], request.data['nit'], request.data['code'])
        with connection.cursor() as cursor:
            cursor.execute(query, values)
        return Response({'message': 'Factura registrada exitosamente'})
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]



class UserRegistrationView(APIView):
    def post(self, request):
        hashed_password = hashlib.sha256(request.data['password'].encode()).hexdigest()
        request.data['password'] = hashed_password
        query = "INSERT INTO core_client (document, first_name, last_name, email, password) VALUES (%s, %s, %s, %s, %s)"
        values = (request.data['document'], request.data['first_name'], request.data['last_name'], request.data['email'], hashed_password)
        with connection.cursor() as cursor:
            cursor.execute(query, values)
        return Response({'message': 'Cliente registrado exitosamente'}, status=status.HTTP_201_CREATED)
        #serializer = ClientSerializer(data=request.data)
        #if serializer.is_valid():
            #client = serializer.save()
            #token_payload = {'user_id': client.id}
            #token = jwt.encode(token_payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM) 
            #return Response({'message': 'Cliente registrado exitosamente', 'token': token}, status=status.HTTP_201_CREATED)
        
        #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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