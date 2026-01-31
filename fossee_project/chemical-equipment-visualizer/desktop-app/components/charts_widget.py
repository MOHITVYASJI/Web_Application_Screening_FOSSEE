"""
Charts Widget for visualizing equipment data using Matplotlib.
Displays bar charts, pie charts, and line charts.
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTabWidget
from PyQt5.QtGui import QFont
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np


class ChartsWidget(QWidget):
    """
    Widget for displaying various charts using Matplotlib.
    Shows equipment distribution, parameter trends, and statistics.
    """
    
    def __init__(self, parent=None):
        """
        Initialize charts widget.
        
        Args:
            parent: Parent widget (optional)
        """
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface."""
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Title
        title_label = QLabel("Data Visualizations")
        title_font = QFont()
        title_font.setPointSize(12)
        title_font.setBold(True)
        title_label.setFont(title_font)
        layout.addWidget(title_label)
        
        # Tab widget for different chart types
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #ddd;
                border-radius: 5px;
                background: white;
            }
            QTabBar::tab {
                background: #f0f0f0;
                padding: 10px 20px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background: white;
                border-bottom: 3px solid #667eea;
            }
        """)
        
        # Create figure canvases for each chart type
        self.distribution_canvas = self._create_canvas()
        self.parameters_canvas = self._create_canvas()
        self.pie_canvas = self._create_canvas()
        
        # Add tabs
        self.tab_widget.addTab(self.distribution_canvas, "Equipment Distribution")
        self.tab_widget.addTab(self.parameters_canvas, "Parameter Comparison")
        self.tab_widget.addTab(self.pie_canvas, "Type Distribution")
        
        layout.addWidget(self.tab_widget)
        self.setLayout(layout)
    
    def _create_canvas(self) -> FigureCanvas:
        """Create a matplotlib canvas."""
        figure = Figure(figsize=(8, 5), dpi=100)
        canvas = FigureCanvas(figure)
        return canvas
    
    def load_data(self, statistics: dict, data: list):
        """
        Load data and create charts.
        
        Args:
            statistics: Dictionary containing summary statistics
            data: List of equipment data records
        """
        if not statistics or not data:
            return
        
        # Create charts
        self._create_distribution_chart(statistics.get('equipment_distribution', {}))
        self._create_parameters_chart(statistics)
        self._create_pie_chart(statistics.get('equipment_distribution', {}))
    
    def _create_distribution_chart(self, distribution: dict):
        """Create bar chart for equipment distribution."""
        figure = self.distribution_canvas.figure
        figure.clear()
        
        if not distribution:
            ax = figure.add_subplot(111)
            ax.text(0.5, 0.5, 'No data available', 
                   ha='center', va='center', fontsize=14, color='gray')
            ax.axis('off')
            self.distribution_canvas.draw()
            return
        
        ax = figure.add_subplot(111)
        
        # Sort by count descending
        items = sorted(distribution.items(), key=lambda x: x[1], reverse=True)
        types = [item[0] for item in items]
        counts = [item[1] for item in items]
        
        # Create bar chart
        colors = plt.cm.Set3(np.linspace(0, 1, len(types)))
        bars = ax.bar(types, counts, color=colors, edgecolor='black', linewidth=0.7)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}',
                   ha='center', va='bottom', fontweight='bold')
        
        ax.set_xlabel('Equipment Type', fontsize=11, fontweight='bold')
        ax.set_ylabel('Count', fontsize=11, fontweight='bold')
        ax.set_title('Equipment Type Distribution', fontsize=13, fontweight='bold', pad=20)
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        
        # Rotate x labels if needed
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        figure.tight_layout()
        self.distribution_canvas.draw()
    
    def _create_parameters_chart(self, statistics: dict):
        """Create grouped bar chart for average parameters."""
        figure = self.parameters_canvas.figure
        figure.clear()
        
        ax = figure.add_subplot(111)
        
        # Extract averages
        params = ['Flowrate', 'Pressure', 'Temperature']
        values = [
            statistics.get('avg_flowrate', 0) or 0,
            statistics.get('avg_pressure', 0) or 0,
            statistics.get('avg_temperature', 0) or 0
        ]
        
        # Create bar chart
        colors = ['#4A90E2', '#50C878', '#FFB347']
        bars = ax.bar(params, values, color=colors, edgecolor='black', linewidth=0.7)
        
        # Add value labels
        for bar, val in zip(bars, values):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{val:.2f}',
                   ha='center', va='bottom', fontweight='bold', fontsize=10)
        
        ax.set_ylabel('Average Value', fontsize=11, fontweight='bold')
        ax.set_title('Average Parameters Comparison', fontsize=13, fontweight='bold', pad=20)
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        
        figure.tight_layout()
        self.parameters_canvas.draw()
    
    def _create_pie_chart(self, distribution: dict):
        """Create pie chart for equipment type distribution."""
        figure = self.pie_canvas.figure
        figure.clear()
        
        if not distribution:
            ax = figure.add_subplot(111)
            ax.text(0.5, 0.5, 'No data available', 
                   ha='center', va='center', fontsize=14, color='gray')
            ax.axis('off')
            self.pie_canvas.draw()
            return
        
        ax = figure.add_subplot(111)
        
        # Sort by count
        items = sorted(distribution.items(), key=lambda x: x[1], reverse=True)
        labels = [item[0] for item in items]
        sizes = [item[1] for item in items]
        
        # Colors
        colors = plt.cm.Set3(np.linspace(0, 1, len(labels)))
        
        # Explode largest slice
        explode = [0.05 if i == 0 else 0 for i in range(len(labels))]
        
        # Create pie chart
        wedges, texts, autotexts = ax.pie(
            sizes, 
            labels=labels, 
            autopct='%1.1f%%',
            startangle=90,
            colors=colors,
            explode=explode,
            shadow=True,
            textprops={'fontsize': 10, 'weight': 'bold'}
        )
        
        # Improve label appearance
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        ax.set_title('Equipment Type Distribution', fontsize=13, fontweight='bold', pad=20)
        ax.axis('equal')  # Equal aspect ratio ensures circular pie
        
        figure.tight_layout()
        self.pie_canvas.draw()
    
    def clear_charts(self):
        """Clear all charts."""
        for canvas in [self.distribution_canvas, self.parameters_canvas, self.pie_canvas]:
            canvas.figure.clear()
            ax = canvas.figure.add_subplot(111)
            ax.text(0.5, 0.5, 'No data loaded', 
                   ha='center', va='center', fontsize=14, color='gray')
            ax.axis('off')
            canvas.draw()
