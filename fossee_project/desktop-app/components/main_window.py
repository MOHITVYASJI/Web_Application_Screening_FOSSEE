"""
Main Window for Chemical Equipment Visualizer Desktop App.
Provides the primary interface for data visualization and analysis.
"""

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFileDialog, QMessageBox, QComboBox, QGroupBox,
    QScrollArea, QFrame, QSplitter, QProgressDialog
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QIcon
import os
from datetime import datetime

from .data_table import DataTableWidget
from .charts_widget import ChartsWidget


class UploadThread(QThread):
    """Background thread for CSV upload to avoid UI freezing."""
    
    upload_complete = pyqtSignal(bool, str, object)  # success, message, dataset
    
    def __init__(self, api_client, file_path):
        super().__init__()
        self.api_client = api_client
        self.file_path = file_path
    
    def run(self):
        """Run upload in background."""
        success, message, dataset = self.api_client.upload_csv(self.file_path)
        self.upload_complete.emit(success, message, dataset)


class MainWindow(QMainWindow):
    """
    Main application window.
    Displays dataset information, statistics, charts, and data table.
    """
    
    def __init__(self, api_client, parent=None):
        """
        Initialize main window.
        
        Args:
            api_client: Authenticated APIClient instance
            parent: Parent widget (optional)
        """
        super().__init__(parent)
        self.api_client = api_client
        self.current_dataset = None
        self.datasets = []
        self.setup_ui()
        self.load_datasets()
    
    def setup_ui(self):
        """Setup the user interface."""
        self.setWindowTitle("Chemical Equipment Visualizer - Desktop")
        self.setMinimumSize(1200, 800)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        # Header
        header_widget = self._create_header()
        main_layout.addWidget(header_widget)
        
        # Upload and dataset selection section
        controls_widget = self._create_controls()
        main_layout.addWidget(controls_widget)
        
        # Statistics cards
        self.statistics_widget = self._create_statistics_section()
        main_layout.addWidget(self.statistics_widget)
        
        # Splitter for charts and data table
        splitter = QSplitter(Qt.Vertical)
        
        # Charts section
        self.charts_widget = ChartsWidget()
        splitter.addWidget(self.charts_widget)
        
        # Data table section
        self.data_table = DataTableWidget()
        splitter.addWidget(self.data_table)
        
        # Set initial sizes (60% charts, 40% table)
        splitter.setSizes([480, 320])
        
        main_layout.addWidget(splitter, stretch=1)
        
        # Apply global styles
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f7fa;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 15px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 8px;
                color: #2c3e50;
            }
            QPushButton {
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 10pt;
            }
            QComboBox {
                padding: 8px;
                border: 2px solid #ddd;
                border-radius: 5px;
                background: white;
                font-size: 10pt;
            }
            QComboBox:focus {
                border-color: #667eea;
            }
        """)
    
    def _create_header(self) -> QWidget:
        """Create header section with title and user info."""
        header = QFrame()
        header.setFrameShape(QFrame.StyledPanel)
        header.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        
        layout = QHBoxLayout(header)
        
        # Title section
        title_layout = QVBoxLayout()
        
        title_label = QLabel("Chemical Equipment Visualizer")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #2c3e50;")
        
        subtitle_label = QLabel("Desktop Application - Data Analysis & Visualization")
        subtitle_label.setStyleSheet("color: #7f8c8d; font-size: 10pt;")
        
        title_layout.addWidget(title_label)
        title_layout.addWidget(subtitle_label)
        
        layout.addLayout(title_layout)
        layout.addStretch()
        
        # User info
        user_info = QLabel(f"User: {self.api_client.user.get('username', 'Unknown')}")
        user_info.setStyleSheet("color: #34495e; font-weight: bold; font-size: 11pt;")
        layout.addWidget(user_info)
        
        # Logout button
        logout_btn = QPushButton("Logout")
        logout_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        logout_btn.clicked.connect(self.handle_logout)
        layout.addWidget(logout_btn)
        
        return header
    
    def _create_controls(self) -> QWidget:
        """Create upload and dataset selection controls."""
        controls = QGroupBox("Dataset Management")
        layout = QHBoxLayout()
        layout.setSpacing(15)
        
        # Upload CSV button
        upload_btn = QPushButton("📁 Upload CSV File")
        upload_btn.setMinimumHeight(45)
        upload_btn.setStyleSheet("""
            QPushButton {
                background-color: #667eea;
                color: white;
            }
            QPushButton:hover {
                background-color: #5568d3;
            }
        """)
        upload_btn.clicked.connect(self.handle_upload)
        layout.addWidget(upload_btn)
        
        # Dataset selector
        layout.addWidget(QLabel("Select Dataset:"))
        self.dataset_combo = QComboBox()
        self.dataset_combo.setMinimumWidth(300)
        self.dataset_combo.setMinimumHeight(45)
        self.dataset_combo.currentIndexChanged.connect(self.handle_dataset_changed)
        layout.addWidget(self.dataset_combo, stretch=1)
        
        # Refresh button
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.setMinimumHeight(45)
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        refresh_btn.clicked.connect(self.load_datasets)
        layout.addWidget(refresh_btn)
        
        # Download PDF button
        self.pdf_btn = QPushButton("📄 Download PDF")
        self.pdf_btn.setMinimumHeight(45)
        self.pdf_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)
        self.pdf_btn.clicked.connect(self.handle_download_pdf)
        self.pdf_btn.setEnabled(False)
        layout.addWidget(self.pdf_btn)
        
        # Delete button
        self.delete_btn = QPushButton("🗑️ Delete")
        self.delete_btn.setMinimumHeight(45)
        self.delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        self.delete_btn.clicked.connect(self.handle_delete)
        self.delete_btn.setEnabled(False)
        layout.addWidget(self.delete_btn)
        
        controls.setLayout(layout)
        return controls
    
    def _create_statistics_section(self) -> QWidget:
        """Create statistics cards section."""
        stats_group = QGroupBox("Summary Statistics")
        layout = QHBoxLayout()
        layout.setSpacing(15)
        
        # Create stat cards
        self.stat_cards = {}
        stats_info = [
            ('total', 'Total Equipment', '0', '#3498db'),
            ('flowrate', 'Avg Flowrate', '0.00', '#27ae60'),
            ('pressure', 'Avg Pressure', '0.00', '#f39c12'),
            ('temperature', 'Avg Temperature', '0.00', '#e74c3c')
        ]
        
        for key, title, default_value, color in stats_info:
            card = self._create_stat_card(title, default_value, color)
            self.stat_cards[key] = card
            layout.addWidget(card)
        
        stats_group.setLayout(layout)
        return stats_group
    
    def _create_stat_card(self, title: str, value: str, color: str) -> QWidget:
        """Create a single statistics card."""
        card = QFrame()
        card.setFrameShape(QFrame.StyledPanel)
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {color};
                border-radius: 8px;
                padding: 15px;
            }}
        """)
        
        layout = QVBoxLayout(card)
        layout.setSpacing(5)
        
        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet("color: white; font-size: 10pt; font-weight: normal;")
        title_label.setAlignment(Qt.AlignCenter)
        
        # Value
        value_label = QLabel(value)
        value_font = QFont()
        value_font.setPointSize(20)
        value_font.setBold(True)
        value_label.setFont(value_font)
        value_label.setStyleSheet("color: white;")
        value_label.setAlignment(Qt.AlignCenter)
        
        layout.addWidget(title_label)
        layout.addWidget(value_label)
        
        # Store value label for updates
        card.value_label = value_label
        
        return card
    
    def load_datasets(self):
        """Load datasets from API."""
        success, message, datasets = self.api_client.get_datasets()
        
        if success and datasets:
            self.datasets = datasets
            self.update_dataset_combo()
            
            # Load first dataset if available
            if self.datasets and not self.current_dataset:
                self.load_dataset_details(self.datasets[0]['id'])
        elif not success:
            QMessageBox.warning(self, "Error", f"Failed to load datasets: {message}")
    
    def update_dataset_combo(self):
        """Update dataset combo box with available datasets."""
        self.dataset_combo.blockSignals(True)
        self.dataset_combo.clear()
        
        for dataset in self.datasets:
            upload_date = dataset.get('uploaded_at', '')
            if upload_date:
                # Format date nicely
                try:
                    dt = datetime.fromisoformat(upload_date.replace('Z', '+00:00'))
                    date_str = dt.strftime('%Y-%m-%d %H:%M')
                except:
                    date_str = upload_date[:16]
            else:
                date_str = 'Unknown date'
            
            label = f"{dataset['name']} - {date_str} ({dataset['total_equipment']} items)"
            self.dataset_combo.addItem(label, dataset['id'])
        
        self.dataset_combo.blockSignals(False)
    
    def handle_dataset_changed(self, index):
        """Handle dataset selection change."""
        if index >= 0:
            dataset_id = self.dataset_combo.itemData(index)
            if dataset_id:
                self.load_dataset_details(dataset_id)
    
    def load_dataset_details(self, dataset_id: int):
        """Load detailed dataset information."""
        success, message, dataset = self.api_client.get_dataset(dataset_id)
        
        if success and dataset:
            self.current_dataset = dataset
            self.update_display()
            self.pdf_btn.setEnabled(True)
            self.delete_btn.setEnabled(True)
        else:
            QMessageBox.warning(self, "Error", f"Failed to load dataset: {message}")
    
    def update_display(self):
        """Update all display elements with current dataset."""
        if not self.current_dataset:
            return
        
        stats = self.current_dataset.get('statistics', {})
        data = self.current_dataset.get('data_json', [])
        
        # Update statistics cards
        self.stat_cards['total'].value_label.setText(str(stats.get('total_equipment', 0)))
        self.stat_cards['flowrate'].value_label.setText(f"{stats.get('avg_flowrate', 0):.2f}")
        self.stat_cards['pressure'].value_label.setText(f"{stats.get('avg_pressure', 0):.2f}")
        self.stat_cards['temperature'].value_label.setText(f"{stats.get('avg_temperature', 0):.2f}")
        
        # Update charts
        self.charts_widget.load_data(stats, data)
        
        # Update data table
        self.data_table.load_data(data)
    
    def handle_upload(self):
        """Handle CSV file upload."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select CSV File",
            "",
            "CSV Files (*.csv);;All Files (*)"
        )
        
        if not file_path:
            return
        
        # Show progress dialog
        progress = QProgressDialog("Uploading and processing CSV file...", None, 0, 0, self)
        progress.setWindowModality(Qt.WindowModal)
        progress.setWindowTitle("Uploading")
        progress.show()
        
        # Upload in background thread
        self.upload_thread = UploadThread(self.api_client, file_path)
        self.upload_thread.upload_complete.connect(
            lambda success, msg, dataset: self.handle_upload_complete(success, msg, dataset, progress)
        )
        self.upload_thread.start()
    
    def handle_upload_complete(self, success, message, dataset, progress):
        """Handle upload completion."""
        progress.close()
        
        if success:
            QMessageBox.information(self, "Success", message)
            self.load_datasets()
            
            # Select the newly uploaded dataset
            if dataset:
                self.current_dataset = dataset
                self.update_display()
        else:
            QMessageBox.critical(self, "Upload Failed", message)
    
    def handle_download_pdf(self):
        """Handle PDF report download."""
        if not self.current_dataset:
            return
        
        # Ask user where to save
        default_name = f"equipment_report_{self.current_dataset['id']}.pdf"
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save PDF Report",
            default_name,
            "PDF Files (*.pdf)"
        )
        
        if not file_path:
            return
        
        # Download PDF
        success, message = self.api_client.download_pdf(self.current_dataset['id'], file_path)
        
        if success:
            QMessageBox.information(self, "Success", message)
        else:
            QMessageBox.critical(self, "Download Failed", message)
    
    def handle_delete(self):
        """Handle dataset deletion."""
        if not self.current_dataset:
            return
        
        # Confirm deletion
        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete '{self.current_dataset['name']}'?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            success, message = self.api_client.delete_dataset(self.current_dataset['id'])
            
            if success:
                QMessageBox.information(self, "Success", message)
                self.current_dataset = None
                self.load_datasets()
                
                # Clear display
                self.stat_cards['total'].value_label.setText('0')
                self.stat_cards['flowrate'].value_label.setText('0.00')
                self.stat_cards['pressure'].value_label.setText('0.00')
                self.stat_cards['temperature'].value_label.setText('0.00')
                self.charts_widget.clear_charts()
                self.data_table.clear_data()
                self.pdf_btn.setEnabled(False)
                self.delete_btn.setEnabled(False)
            else:
                QMessageBox.critical(self, "Deletion Failed", message)
    
    def handle_logout(self):
        """Handle user logout."""
        reply = QMessageBox.question(
            self,
            "Confirm Logout",
            "Are you sure you want to logout?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.close()
