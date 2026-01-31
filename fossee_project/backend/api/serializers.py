"""
Django REST Framework serializers for API data validation and transformation.

Serializers handle:
- User registration and authentication
- Dataset upload and validation
- Statistics presentation
- Data format conversion (model <-> JSON)
"""

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Dataset
import pandas as pd
from io import StringIO


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Handles user registration with password confirmation.
    """
    password = serializers.CharField(write_only=True, min_length=6)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 'first_name', 'last_name']
        extra_kwargs = {
            'email': {'required': True},
        }
    
    def validate(self, data):
        """Validate that passwords match."""
        if data['password'] != data.get('password_confirm'):
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return data
    
    def create(self, validated_data):
        """Create user with hashed password."""
        validated_data.pop('password_confirm')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    """
    Basic user information for API responses.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class DatasetListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing datasets (without full data).
    Shows summary information only for performance.
    """
    user = serializers.StringRelatedField()
    record_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Dataset
        fields = [
            'id', 'name', 'user', 'uploaded_at', 'total_equipment',
            'avg_flowrate', 'avg_pressure', 'avg_temperature',
            'equipment_distribution', 'record_count'
        ]
        read_only_fields = ['id', 'user', 'uploaded_at']


class DatasetDetailSerializer(serializers.ModelSerializer):
    """
    Detailed dataset serializer including full data.
    Used when retrieving a specific dataset.
    """
    user = UserSerializer(read_only=True)
    statistics = serializers.SerializerMethodField()
    
    class Meta:
        model = Dataset
        fields = [
            'id', 'name', 'user', 'uploaded_at', 'file',
            'data_json', 'statistics', 'total_equipment'
        ]
        read_only_fields = ['id', 'user', 'uploaded_at']
    
    def get_statistics(self, obj):
        """Include pre-calculated statistics."""
        return obj.get_statistics_summary()


class DatasetUploadSerializer(serializers.Serializer):
    """
    Handles CSV file upload and validation.
    
    Validation steps:
    1. Check file extension is .csv
    2. Validate CSV structure
    3. Check required columns exist
    4. Validate data types
    5. Handle missing values
    """
    file = serializers.FileField()
    
    # Required columns in CSV (accepts both underscore and space versions)
    REQUIRED_COLUMNS = ['Equipment_Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']
    REQUIRED_COLUMNS_ALT = ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']
    
    def validate_file(self, file):
        """
        Validate uploaded CSV file.
        Accepts both "Equipment_Name" and "Equipment Name" column formats.
        """
        # Check file extension
        if not file.name.endswith('.csv'):
            raise serializers.ValidationError(
                "Invalid file format. Please upload a CSV file."
            )
        
        # Check file size (max 5MB)
        if file.size > 5 * 1024 * 1024:
            raise serializers.ValidationError(
                "File size exceeds 5MB limit."
            )
        
        try:
            # Read CSV file
            file.seek(0)  # Reset file pointer
            content = file.read().decode('utf-8')
            df = pd.read_csv(StringIO(content))
            
            # Check if file is empty
            if df.empty:
                raise serializers.ValidationError(
                    "CSV file is empty. Please upload a file with data."
                )
            
            # Clean column names
            df.columns = df.columns.str.strip()
            
            # Normalize column names for validation
            normalized_columns = [col.replace(' ', '_') for col in df.columns]
            
            # Validate required columns (check normalized version)
            missing_columns = set(self.REQUIRED_COLUMNS) - set(normalized_columns)
            if missing_columns:
                raise serializers.ValidationError(
                    f"Missing required columns: {', '.join(missing_columns)}. "
                    f"Required columns are: Equipment Name (or Equipment_Name), Type, Flowrate, Pressure, Temperature. "
                    f"Found columns: {', '.join(df.columns)}"
                )
            
            # Validate numeric columns
            numeric_columns = ['Flowrate', 'Pressure', 'Temperature']
            for col in numeric_columns:
                try:
                    pd.to_numeric(df[col], errors='raise')
                except (ValueError, TypeError):
                    raise serializers.ValidationError(
                        f"Column '{col}' must contain numeric values only."
                    )
            
            # Check for too many missing values
            for col in self.REQUIRED_COLUMNS:
                missing_pct = df[col].isna().sum() / len(df) * 100
                if missing_pct > 50:
                    raise serializers.ValidationError(
                        f"Column '{col}' has {missing_pct:.1f}% missing values. "
                        "Please provide a cleaner dataset."
                    )
            
            # Reset file pointer for later use
            file.seek(0)
            
        except pd.errors.EmptyDataError:
            raise serializers.ValidationError(
                "CSV file is empty or corrupted."
            )
        except pd.errors.ParserError:
            raise serializers.ValidationError(
                "Unable to parse CSV file. Please check the file format."
            )
        except Exception as e:
            raise serializers.ValidationError(
                f"Error processing CSV file: {str(e)}"
            )
        
        return file


class StatisticsSerializer(serializers.Serializer):
    """
    Serializer for dataset statistics response.
    """
    total_equipment = serializers.IntegerField()
    avg_flowrate = serializers.FloatField()
    avg_pressure = serializers.FloatField()
    avg_temperature = serializers.FloatField()
    equipment_distribution = serializers.DictField()