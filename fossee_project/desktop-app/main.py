#!/usr/bin/env python3
"""
Chemical Equipment Parameter Visualizer - Desktop Application
Main entry point for the PyQt5 desktop application.

This application provides:
- User authentication
- CSV file upload and processing
- Data visualization with charts (Matplotlib)
- Statistics display
- PDF report generation
- Dataset history management

Requirements:
- Python 3.8+
- PyQt5
- Matplotlib
- Requests
- Backend server running at http://localhost:8000

Usage:
    python main.py [--server SERVER_URL]

Author: FOSSEE Screening Task
"""

import sys
import argparse
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import Qt

# Import custom components
from components.login_window import LoginWindow
from components.main_window import MainWindow
from utils.api_client import APIClient


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Chemical Equipment Visualizer - Desktop Application'
    )
    parser.add_argument(
        '--server',
        default='http://localhost:8000/api',
        help='Backend server URL (default: http://localhost:8000/api)'
    )
    return parser.parse_args()


class Application:
    """
    Main application class.
    Manages application lifecycle and window transitions.
    """
    
    def __init__(self, server_url: str):
        """
        Initialize application.
        
        Args:
            server_url: Backend API base URL
        """
        self.api_client = APIClient(base_url=server_url)
        self.login_window = None
        self.main_window = None
        
    def start(self):
        """Start the application by showing login window."""
        self.login_window = LoginWindow(self.api_client)
        self.login_window.login_successful.connect(self.show_main_window)
        
        # Show login window
        result = self.login_window.exec_()
        
        # If login cancelled, exit application
        if result == LoginWindow.Rejected:
            sys.exit(0)
    
    def show_main_window(self, api_client):
        """
        Show main application window after successful login.
        
        Args:
            api_client: Authenticated APIClient instance
        """
        try:
            self.main_window = MainWindow(api_client)
            self.main_window.show()
        except Exception as e:
            QMessageBox.critical(
                None,
                "Error",
                f"Failed to start main application: {str(e)}"
            )
            sys.exit(1)


def main():
    """Main entry point."""
    # Parse command line arguments
    args = parse_arguments()
    
    # Create Qt application
    app = QApplication(sys.argv)
    app.setApplicationName("Chemical Equipment Visualizer")
    app.setOrganizationName("FOSSEE")
    app.setApplicationVersion("1.0.0")
    
    # Set application style
    app.setStyle('Fusion')
    
    # Enable High DPI scaling
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    # Print startup information
    print("=" * 60)
    print("Chemical Equipment Parameter Visualizer")
    print("Desktop Application v1.0.0")
    print("=" * 60)
    print(f"Backend Server: {args.server}")
    print("Starting application...")
    print("=" * 60)
    
    # Create and start application
    application = Application(args.server)
    application.start()
    
    # Run application event loop
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
