"""
Data Table Widget for displaying CSV data in a table format.
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QHeaderView, QLabel, QHBoxLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class DataTableWidget(QWidget):
    """
    Widget for displaying dataset in a table format.
    Shows equipment data with all columns.
    """
    
    def __init__(self, parent=None):
        """
        Initialize data table widget.
        
        Args:
            parent: Parent widget (optional)
        """
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the user interface."""
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Header
        header_layout = QHBoxLayout()
        self.title_label = QLabel("Equipment Data")
        title_font = QFont()
        title_font.setPointSize(12)
        title_font.setBold(True)
        self.title_label.setFont(title_font)
        header_layout.addWidget(self.title_label)
        
        self.count_label = QLabel("0 records")
        self.count_label.setStyleSheet("color: #666;")
        header_layout.addWidget(self.count_label)
        header_layout.addStretch()
        
        layout.addLayout(header_layout)
        
        # Table
        self.table = QTableWidget()
        self.table.setAlternatingRowColors(True)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.horizontalHeader().setStretchLastSection(True)
        
        # Style the table
        self.table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #ddd;
                border-radius: 5px;
                background-color: white;
                gridline-color: #e0e0e0;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QTableWidget::item:selected {
                background-color: #667eea;
                color: white;
            }
            QHeaderView::section {
                background-color: #f0f0f0;
                padding: 10px;
                border: none;
                border-right: 1px solid #ddd;
                border-bottom: 2px solid #667eea;
                font-weight: bold;
            }
        """)
        
        layout.addWidget(self.table)
        self.setLayout(layout)
    
    def load_data(self, data: list):
        """
        Load data into the table.
        
        Args:
            data: List of dictionaries containing equipment data
        """
        if not data:
            self.table.setRowCount(0)
            self.table.setColumnCount(0)
            self.count_label.setText("0 records")
            return
        
        # Update count
        self.count_label.setText(f"{len(data)} records")
        
        # Get column names from first record
        columns = list(data[0].keys())
        
        # Setup table
        self.table.setRowCount(len(data))
        self.table.setColumnCount(len(columns))
        self.table.setHorizontalHeaderLabels(columns)
        
        # Populate table
        for row_idx, record in enumerate(data):
            for col_idx, column in enumerate(columns):
                value = record.get(column, '')
                
                # Format numeric values
                if isinstance(value, float):
                    value = f"{value:.2f}"
                elif value is None:
                    value = 'N/A'
                else:
                    value = str(value)
                
                item = QTableWidgetItem(value)
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row_idx, col_idx, item)
        
        # Resize columns to content
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setStretchLastSection(True)
    
    def clear_data(self):
        """Clear all data from table."""
        self.table.setRowCount(0)
        self.table.setColumnCount(0)
        self.count_label.setText("0 records")
