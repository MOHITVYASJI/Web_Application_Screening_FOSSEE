"""
Django REST Framework views for Chemical Equipment Visualizer API.

API Endpoints:
1. Authentication: register, login (JWT tokens)
2. Dataset management: upload, list, retrieve, delete
3. Statistics: get calculated statistics for a dataset
4. PDF generation: download report for a dataset
"""

from rest_framework import viewsets, status, generics
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.conf import settings
from django.http import FileResponse, HttpResponse
from django.db.models import Q

from .models import Dataset
from .serializers import (
    UserRegistrationSerializer,
    UserSerializer,
    DatasetListSerializer,
    DatasetDetailSerializer,
    DatasetUploadSerializer,
    StatisticsSerializer
)
from .utils import (
    parse_csv_file,
    calculate_statistics,
    dataframe_to_json,
    generate_pdf_report
)

import logging

logger = logging.getLogger(__name__)


# ==================== Authentication Views ====================

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """
    Register a new user and return JWT tokens.
    
    Expected payload:
    {
        "username": "john_doe",
        "email": "john@example.com",
        "password": "secure_password",
        "password_confirm": "secure_password",
        "first_name": "John",
        "last_name": "Doe"
    }
    """
    serializer = UserRegistrationSerializer(data=request.data)
    
    if serializer.is_valid():
        try:
            user = serializer.save()
            
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'message': 'User registered successfully',
                'user': UserSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            logger.error(f"Registration error: {str(e)}")
            return Response(
                {'error': 'Registration failed. Please try again.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    """
    Authenticate user and return JWT tokens.
    
    Expected payload:
    {
        "username": "john_doe",
        "password": "secure_password"
    }
    """
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response(
            {'error': 'Please provide both username and password'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Authenticate user
    user = authenticate(username=username, password=password)
    
    if user is not None:
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'message': 'Login successful',
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_200_OK)
    
    return Response(
        {'error': 'Invalid credentials'},
        status=status.HTTP_401_UNAUTHORIZED
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    """
    Get current authenticated user details.
    """
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


# ==================== Dataset Views ====================

class DatasetViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing datasets.
    
    Actions:
    - list: Get all datasets for current user (last 5)
    - retrieve: Get specific dataset details
    - upload: Upload new CSV file
    - destroy: Delete a dataset
    - statistics: Get statistics for a dataset
    - download_pdf: Generate and download PDF report
    """
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Return datasets for the current user only.
        Limited to last 5 datasets as per requirements.
        """
        return Dataset.objects.filter(user=self.request.user).order_by('-uploaded_at')[:5]
    
    def get_serializer_class(self):
        """
        Use different serializers for list and detail views.
        """
        if self.action == 'list':
            return DatasetListSerializer
        return DatasetDetailSerializer
    
    def list(self, request):
        """
        List all datasets for the current user (last 5).
        """
        queryset = Dataset.objects.filter(user=request.user).order_by('-uploaded_at')[:5]
        serializer = DatasetListSerializer(queryset, many=True)
        
        return Response({
            'count': queryset.count(),
            'results': serializer.data
        })
    
    def retrieve(self, request, pk=None):
        """
        Get detailed information about a specific dataset.
        """
        try:
            dataset = Dataset.objects.get(pk=pk, user=request.user)
            serializer = DatasetDetailSerializer(dataset)
            return Response(serializer.data)
        except Dataset.DoesNotExist:
            return Response(
                {'error': 'Dataset not found'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['post'])
    def upload(self, request):
        """
        Upload and process a new CSV file.
        
        Steps:
        1. Validate CSV file format
        2. Parse CSV using Pandas
        3. Calculate statistics
        4. Save to database
        5. Maintain only last 5 datasets (delete older ones)
        """
        serializer = DatasetUploadSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            csv_file = serializer.validated_data['file']
            
            # Parse CSV file
            df, metadata = parse_csv_file(csv_file)
            
            # Calculate statistics
            stats = calculate_statistics(df)
            
            # Convert DataFrame to JSON
            data_json = dataframe_to_json(df)
            
            # Create dataset instance
            dataset = Dataset.objects.create(
                user=request.user,
                name=csv_file.name,
                file=csv_file,
                data_json=data_json,
                total_equipment=stats['total_equipment'],
                avg_flowrate=stats['avg_flowrate'],
                avg_pressure=stats['avg_pressure'],
                avg_temperature=stats['avg_temperature'],
                equipment_distribution=stats['equipment_distribution']
            )
            
            # Maintain only last 5 datasets per user
            user_datasets = Dataset.objects.filter(user=request.user).order_by('-uploaded_at')
            
            if user_datasets.count() > settings.MAX_DATASETS_PER_USER:
                # Delete oldest datasets beyond the limit
                datasets_to_delete = user_datasets[settings.MAX_DATASETS_PER_USER:]
                for old_dataset in datasets_to_delete:
                    old_dataset.file.delete()  # Delete file from storage
                    old_dataset.delete()  # Delete database record
            
            # Return success response with dataset details
            response_serializer = DatasetDetailSerializer(dataset)
            
            return Response({
                'message': 'Dataset uploaded and processed successfully',
                'dataset': response_serializer.data
            }, status=status.HTTP_201_CREATED)
            
        except ValueError as e:
            logger.error(f"CSV parsing error: {str(e)}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Upload error: {str(e)}")
            return Response(
                {'error': 'An error occurred while processing the file. Please try again.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def destroy(self, request, pk=None):
        """
        Delete a dataset.
        """
        try:
            dataset = Dataset.objects.get(pk=pk, user=request.user)
            
            # Delete file from storage
            if dataset.file:
                dataset.file.delete()
            
            dataset.delete()
            
            return Response(
                {'message': 'Dataset deleted successfully'},
                status=status.HTTP_204_NO_CONTENT
            )
        except Dataset.DoesNotExist:
            return Response(
                {'error': 'Dataset not found'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['get'])
    def statistics(self, request, pk=None):
        """
        Get calculated statistics for a specific dataset.
        """
        try:
            dataset = Dataset.objects.get(pk=pk, user=request.user)
            stats = dataset.get_statistics_summary()
            
            return Response(stats)
        except Dataset.DoesNotExist:
            return Response(
                {'error': 'Dataset not found'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['get'])
    def download_pdf(self, request, pk=None):
        """
        Generate and download a PDF report for the dataset.
        
        The PDF includes:
        - Dataset metadata
        - Summary statistics
        - Equipment distribution table and chart
        - Data preview
        """
        try:
            dataset = Dataset.objects.get(pk=pk, user=request.user)
            
            # Generate PDF
            pdf_buffer = generate_pdf_report(dataset)
            
            # Create response with PDF
            response = HttpResponse(pdf_buffer.read(), content_type='application/pdf')
            filename = f"equipment_report_{dataset.id}_{dataset.uploaded_at.strftime('%Y%m%d')}.pdf"
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            
            return response
            
        except Dataset.DoesNotExist:
            return Response(
                {'error': 'Dataset not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"PDF generation error: {str(e)}")
            return Response(
                {'error': 'Failed to generate PDF report'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )