"""
API Client for communicating with Django backend.
Handles authentication, dataset operations, and file uploads.
"""

import requests
import json
from typing import Optional, Dict, Any, Tuple


class APIClient:
    """
    Client for interacting with Chemical Equipment Visualizer API.
    
    Handles:
    - Authentication (login, token management)
    - Dataset operations (upload, list, retrieve, delete)
    - Statistics retrieval
    - PDF download
    """
    
    def __init__(self, base_url: str = "http://localhost:8000/api"):
        """
        Initialize API client.
        
        Args:
            base_url: Base URL of the API
        """
        self.base_url = base_url.rstrip('/')
        self.access_token: Optional[str] = None
        self.refresh_token: Optional[str] = None
        self.user: Optional[Dict] = None
        
    def _get_headers(self) -> Dict[str, str]:
        """Get headers with authentication token."""
        headers = {'Content-Type': 'application/json'}
        if self.access_token:
            headers['Authorization'] = f'Bearer {self.access_token}'
        return headers
    
    def login(self, username: str, password: str) -> Tuple[bool, str]:
        """
        Authenticate user and store tokens.
        
        Args:
            username: User's username
            password: User's password
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            response = requests.post(
                f'{self.base_url}/auth/login/',
                json={'username': username, 'password': password},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                self.access_token = data['tokens']['access']
                self.refresh_token = data['tokens']['refresh']
                self.user = data['user']
                return True, "Login successful"
            else:
                error_msg = response.json().get('error', 'Login failed')
                return False, error_msg
                
        except requests.exceptions.ConnectionError:
            return False, "Cannot connect to server. Please ensure backend is running."
        except requests.exceptions.Timeout:
            return False, "Request timed out. Please try again."
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def register(self, username: str, email: str, password: str, 
                 first_name: str = "", last_name: str = "") -> Tuple[bool, str]:
        """
        Register a new user.
        
        Args:
            username: Desired username
            email: User's email
            password: User's password
            first_name: User's first name (optional)
            last_name: User's last name (optional)
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            data = {
                'username': username,
                'email': email,
                'password': password,
                'password_confirm': password,
                'first_name': first_name,
                'last_name': last_name
            }
            
            response = requests.post(
                f'{self.base_url}/auth/register/',
                json=data,
                timeout=10
            )
            
            if response.status_code == 201:
                data = response.json()
                self.access_token = data['tokens']['access']
                self.refresh_token = data['tokens']['refresh']
                self.user = data['user']
                return True, "Registration successful"
            else:
                errors = response.json()
                error_msg = '. '.join([f"{k}: {v[0] if isinstance(v, list) else v}" 
                                       for k, v in errors.items()])
                return False, error_msg
                
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def upload_csv(self, file_path: str) -> Tuple[bool, str, Optional[Dict]]:
        """
        Upload CSV file to backend.
        
        Args:
            file_path: Path to CSV file
            
        Returns:
            Tuple of (success: bool, message: str, dataset: Optional[Dict])
        """
        try:
            with open(file_path, 'rb') as f:
                files = {'file': f}
                headers = {}
                if self.access_token:
                    headers['Authorization'] = f'Bearer {self.access_token}'
                
                response = requests.post(
                    f'{self.base_url}/datasets/upload/',
                    files=files,
                    headers=headers,
                    timeout=30
                )
            
            if response.status_code == 201:
                data = response.json()
                return True, data['message'], data['dataset']
            else:
                error_data = response.json()
                error_msg = error_data.get('error', 
                           error_data.get('file', ['Upload failed'])[0] if 'file' in error_data else 'Upload failed')
                return False, error_msg, None
                
        except FileNotFoundError:
            return False, "File not found", None
        except Exception as e:
            return False, f"Error: {str(e)}", None
    
    def get_datasets(self) -> Tuple[bool, str, Optional[list]]:
        """
        Get list of user's datasets (last 5).
        
        Returns:
            Tuple of (success: bool, message: str, datasets: Optional[list])
        """
        try:
            response = requests.get(
                f'{self.base_url}/datasets/',
                headers=self._get_headers(),
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                return True, "Success", data.get('results', [])
            else:
                return False, "Failed to fetch datasets", None
                
        except Exception as e:
            return False, f"Error: {str(e)}", None
    
    def get_dataset(self, dataset_id: int) -> Tuple[bool, str, Optional[Dict]]:
        """
        Get detailed information about a specific dataset.
        
        Args:
            dataset_id: ID of the dataset
            
        Returns:
            Tuple of (success: bool, message: str, dataset: Optional[Dict])
        """
        try:
            response = requests.get(
                f'{self.base_url}/datasets/{dataset_id}/',
                headers=self._get_headers(),
                timeout=10
            )
            
            if response.status_code == 200:
                return True, "Success", response.json()
            else:
                return False, "Dataset not found", None
                
        except Exception as e:
            return False, f"Error: {str(e)}", None
    
    def delete_dataset(self, dataset_id: int) -> Tuple[bool, str]:
        """
        Delete a dataset.
        
        Args:
            dataset_id: ID of the dataset to delete
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            response = requests.delete(
                f'{self.base_url}/datasets/{dataset_id}/',
                headers=self._get_headers(),
                timeout=10
            )
            
            if response.status_code == 204:
                return True, "Dataset deleted successfully"
            else:
                return False, "Failed to delete dataset"
                
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def download_pdf(self, dataset_id: int, save_path: str) -> Tuple[bool, str]:
        """
        Download PDF report for a dataset.
        
        Args:
            dataset_id: ID of the dataset
            save_path: Path where to save the PDF
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            response = requests.get(
                f'{self.base_url}/datasets/{dataset_id}/download_pdf/',
                headers=self._get_headers(),
                timeout=30
            )
            
            if response.status_code == 200:
                with open(save_path, 'wb') as f:
                    f.write(response.content)
                return True, f"PDF saved to {save_path}"
            else:
                return False, "Failed to download PDF"
                
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def is_authenticated(self) -> bool:
        """Check if user is authenticated."""
        return self.access_token is not None
