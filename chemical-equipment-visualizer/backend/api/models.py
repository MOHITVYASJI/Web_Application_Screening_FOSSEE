"""
Django models for Chemical Equipment Visualizer.

Dataset model stores:
- User who uploaded the file
- CSV file path
- Parsed data in JSON format
- Pre-calculated statistics for quick retrieval
- Equipment type distribution
- Timestamp for automatic cleanup of old datasets
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import json


class Dataset(models.Model):
    """
    Represents an uploaded CSV dataset with its metadata and statistics.
    
    Business Logic:
    - Each user can have maximum 5 datasets (enforced in views)
    - Older datasets are automatically deleted when limit is exceeded
    - Statistics are pre-calculated on upload for performance
    - Original data is stored as JSON for quick access
    """
    
    # Relationships
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='datasets',
        help_text="User who uploaded this dataset"
    )
    
    # File information
    name = models.CharField(
        max_length=255,
        help_text="Original filename of uploaded CSV"
    )
    file = models.FileField(
        upload_to='datasets/%Y/%m/%d/',
        help_text="Uploaded CSV file"
    )
    uploaded_at = models.DateTimeField(
        default=timezone.now,
        help_text="Timestamp when dataset was uploaded"
    )
    
    # Parsed data (stored as JSON for easy retrieval)
    data_json = models.JSONField(
        help_text="Complete dataset in JSON format"
    )
    
    # Pre-calculated statistics
    total_equipment = models.IntegerField(
        default=0,
        help_text="Total number of equipment records"
    )
    avg_flowrate = models.FloatField(
        null=True, 
        blank=True,
        help_text="Average flowrate across all equipment"
    )
    avg_pressure = models.FloatField(
        null=True, 
        blank=True,
        help_text="Average pressure across all equipment"
    )
    avg_temperature = models.FloatField(
        null=True, 
        blank=True,
        help_text="Average temperature across all equipment"
    )
    
    # Equipment distribution (stored as JSON)
    # Format: {"Pump": 5, "Valve": 3, "Reactor": 2}
    equipment_distribution = models.JSONField(
        default=dict,
        help_text="Count of each equipment type"
    )
    
    class Meta:
        ordering = ['-uploaded_at']  # Newest first
        verbose_name = 'Dataset'
        verbose_name_plural = 'Datasets'
        indexes = [
            models.Index(fields=['user', '-uploaded_at']),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.user.username} ({self.uploaded_at.strftime('%Y-%m-%d %H:%M')})"
    
    def get_statistics_summary(self):
        """
        Returns a dictionary with all statistics for API responses.
        """
        return {
            'total_equipment': self.total_equipment,
            'avg_flowrate': round(self.avg_flowrate, 2) if self.avg_flowrate else None,
            'avg_pressure': round(self.avg_pressure, 2) if self.avg_pressure else None,
            'avg_temperature': round(self.avg_temperature, 2) if self.avg_temperature else None,
            'equipment_distribution': self.equipment_distribution,
        }
    
    def get_data_preview(self, limit=10):
        """
        Returns first N records for preview.
        """
        if isinstance(self.data_json, list):
            return self.data_json[:limit]
        return []
    
    @property
    def record_count(self):
        """Returns the number of records in the dataset."""
        if isinstance(self.data_json, list):
            return len(self.data_json)
        return 0