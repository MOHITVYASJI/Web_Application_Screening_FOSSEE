"""
Login Window for Chemical Equipment Visualizer Desktop App.
Provides authentication interface for users.
"""

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox, QGroupBox, QFormLayout
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QIcon


class LoginWindow(QDialog):
    """
    Login dialog for user authentication.
    Emits login_successful signal when user successfully logs in.
    """
    
    login_successful = pyqtSignal(object)  # Emits API client
    
    def __init__(self, api_client, parent=None):
        """
        Initialize login window.
        
        Args:
            api_client: APIClient instance for authentication
            parent: Parent widget (optional)
        """
        super().__init__(parent)
        self.api_client = api_client
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface."""
        self.setWindowTitle("Chemical Equipment Visualizer - Login")
        self.setFixedSize(450, 350)
        self.setModal(True)
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        
        # Title
        title_label = QLabel("Chemical Equipment Visualizer")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        subtitle_label = QLabel("Desktop Application")
        subtitle_font = QFont()
        subtitle_font.setPointSize(10)
        subtitle_label.setFont(subtitle_font)
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("color: #666;")
        main_layout.addWidget(subtitle_label)
        
        main_layout.addSpacing(10)
        
        # Login form group
        login_group = QGroupBox("Login Credentials")
        login_layout = QFormLayout()
        login_layout.setSpacing(15)
        
        # Username field
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username")
        self.username_input.setMinimumHeight(35)
        login_layout.addRow("Username:", self.username_input)
        
        # Password field
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setMinimumHeight(35)
        self.password_input.returnPressed.connect(self.handle_login)
        login_layout.addRow("Password:", self.password_input)
        
        login_group.setLayout(login_layout)
        main_layout.addWidget(login_group)
        
        # Backend URL info
        url_label = QLabel(f"Server: {self.api_client.base_url}")
        url_label.setStyleSheet("color: #888; font-size: 9pt;")
        url_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(url_label)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        self.login_button = QPushButton("Login")
        self.login_button.setMinimumHeight(40)
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #667eea;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
                font-size: 11pt;
            }
            QPushButton:hover {
                background-color: #5568d3;
            }
            QPushButton:pressed {
                background-color: #4451b8;
            }
        """)
        self.login_button.clicked.connect(self.handle_login)
        
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setMinimumHeight(40)
        self.cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #e0e0e0;
                color: #333;
                border: none;
                border-radius: 5px;
                font-weight: bold;
                font-size: 11pt;
            }
            QPushButton:hover {
                background-color: #d0d0d0;
            }
        """)
        self.cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(self.login_button)
        button_layout.addWidget(self.cancel_button)
        
        main_layout.addLayout(button_layout)
        
        # Note about registration
        note_label = QLabel("Note: Register via web interface if you don't have an account")
        note_label.setStyleSheet("color: #999; font-size: 8pt; font-style: italic;")
        note_label.setAlignment(Qt.AlignCenter)
        note_label.setWordWrap(True)
        main_layout.addWidget(note_label)
        
        main_layout.addStretch()
        
        self.setLayout(main_layout)
        
        # Style the dialog
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f5f5;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #ddd;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
            QLineEdit {
                border: 2px solid #ddd;
                border-radius: 5px;
                padding: 8px;
                font-size: 10pt;
            }
            QLineEdit:focus {
                border-color: #667eea;
            }
        """)
    
    def handle_login(self):
        """Handle login button click."""
        username = self.username_input.text().strip()
        password = self.password_input.text()
        
        # Validate inputs
        if not username:
            QMessageBox.warning(self, "Validation Error", "Please enter your username.")
            self.username_input.setFocus()
            return
        
        if not password:
            QMessageBox.warning(self, "Validation Error", "Please enter your password.")
            self.password_input.setFocus()
            return
        
        # Disable button during login
        self.login_button.setEnabled(False)
        self.login_button.setText("Logging in...")
        
        # Attempt login
        success, message = self.api_client.login(username, password)
        
        # Re-enable button
        self.login_button.setEnabled(True)
        self.login_button.setText("Login")
        
        if success:
            QMessageBox.information(self, "Success", message)
            self.login_successful.emit(self.api_client)
            self.accept()
        else:
            QMessageBox.critical(self, "Login Failed", message)
            self.password_input.clear()
            self.password_input.setFocus()
