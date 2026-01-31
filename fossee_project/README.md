# Chemical Equipment Parameter Visualizer

## Project Overview

A hybrid Web + Desktop application for visualizing and analyzing chemical equipment parameters. Built for FOSSEE Semester-long Internship screening task.

### Features
- CSV file upload for chemical equipment data
- Real-time data parsing and analysis using Pandas
- Summary statistics (total count, averages, distribution)
- Interactive data visualizations (Web: Chart.js, Desktop: Matplotlib)
- History management (last 5 datasets)
- PDF report generation with charts and statistics
- JWT-based authentication
- Responsive web interface and native desktop application

### Tech Stack

**Backend:**
- Django 4.2.7
- Django REST Framework 3.14.0
- Pandas for data processing
- SQLite database
- ReportLab for PDF generation

**Web Frontend:**
- React.js 18
- Chart.js for visualizations
- Axios for API communication
- Material-UI components

**Desktop Frontend:**
- PyQt5
- Matplotlib for charts
- Python requests library

## Project Structure

```
chemical-equipment-visualizer/
├── backend/                    # Django backend
│   ├── config/                # Project settings
│   ├── api/                   # Main API app
│   ├── media/                 # Uploaded files
│   ├── manage.py
│   └── requirements.txt
├── web-frontend/              # React application
│   ├── src/
│   ├── public/
│   └── package.json
├── desktop-app/               # PyQt5 application
│   ├── main.py
│   ├── components/
│   └── requirements.txt
├── sample_equipment_data.csv  # Sample CSV file
└── README.md
```

## Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn
- Git

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Create superuser (optional):
```bash
python manage.py createsuperuser
```

6. Start development server:
```bash
python manage.py runserver
```

Backend will run at: `http://localhost:8000`

### Web Frontend Setup

1. Navigate to web-frontend directory:
```bash
cd web-frontend
```

2. Install dependencies:
```bash
npm install
# or
yarn install
```

3. Start development server:
```bash
npm start
# or
yarn start
```

Web app will run at: `http://localhost:3000`

### Desktop Application Setup

1. Navigate to desktop-app directory:
```bash
cd desktop-app
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

## Usage Guide

### CSV File Format

The CSV file should contain the following columns:
- **Equipment_Name**: Name of the equipment (string)
- **Type**: Type/category of equipment (string)
- **Flowrate**: Flow rate value (numeric)
- **Pressure**: Pressure value (numeric)
- **Temperature**: Temperature value (numeric)

Example:
```csv
Equipment_Name,Type,Flowrate,Pressure,Temperature
Pump-101,Pump,150.5,25.3,75.2
Valve-201,Valve,200.0,30.5,80.1
```

### Web Application Flow

1. **Register/Login**: Create account or login with credentials
2. **Upload CSV**: Click upload button and select CSV file
3. **View Data**: Browse uploaded data in interactive table
4. **Analyze**: View summary statistics and charts
5. **Download Report**: Generate and download PDF report
6. **History**: Access last 5 uploaded datasets

### Desktop Application Flow

1. **Login**: Enter credentials and connect to backend
2. **Upload CSV**: Use file dialog to select CSV file
3. **View Results**: See data table, statistics, and charts
4. **Download Report**: Save PDF report locally

## API Endpoints

### Authentication
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login and get JWT token
- `POST /api/auth/refresh/` - Refresh JWT token

### Datasets
- `GET /api/datasets/` - List all datasets (last 5)
- `POST /api/datasets/upload/` - Upload new CSV file
- `GET /api/datasets/{id}/` - Get specific dataset details
- `GET /api/datasets/{id}/statistics/` - Get dataset statistics
- `GET /api/datasets/{id}/download-pdf/` - Download PDF report
- `DELETE /api/datasets/{id}/` - Delete dataset

## Features Explained

### 1. CSV Upload & Validation
- Validates CSV structure and required columns
- Checks data types and handles missing values
- Provides detailed error messages

### 2. Data Analysis
- **Total Equipment Count**: Number of equipment records
- **Average Flowrate**: Mean value across all equipment
- **Average Pressure**: Mean pressure value
- **Average Temperature**: Mean temperature value
- **Equipment Distribution**: Count by equipment type

### 3. History Management
- Automatically maintains last 5 datasets per user
- Older datasets are automatically deleted
- Each dataset stores metadata and statistics

### 4. PDF Report Generation
- Summary statistics table
- Equipment type distribution chart
- Parameter trend charts
- Dataset metadata (upload date, record count)

### 5. Visualizations
- **Bar Chart**: Equipment type distribution
- **Line Chart**: Parameter trends
- **Pie Chart**: Equipment type percentage
- **Table View**: Complete dataset with pagination

## Technical Decisions & Best Practices

### Backend
1. **Django REST Framework**: Industry-standard for building APIs
2. **JWT Authentication**: Secure, stateless authentication
3. **Pandas**: Efficient CSV parsing and data analysis
4. **SQLite**: Lightweight, zero-configuration database
5. **Model Validation**: Ensures data integrity
6. **CORS Configuration**: Enables cross-origin requests

### Frontend (Web)
1. **Component-Based Architecture**: Reusable, maintainable code
2. **State Management**: React hooks for local state
3. **Error Boundaries**: Graceful error handling
4. **Responsive Design**: Works on all screen sizes
5. **Loading States**: Better user experience

### Desktop Application
1. **Qt Widgets**: Native-looking UI components
2. **Threading**: Non-blocking API requests
3. **Matplotlib Integration**: High-quality charts
4. **Error Dialogs**: User-friendly error messages

## Testing

### Backend Tests
```bash
cd backend
python manage.py test
```

### Frontend Tests
```bash
cd web-frontend
npm test
```

## Deployment

### Backend Deployment (Production)
1. Set `DEBUG = False` in settings.py
2. Configure `ALLOWED_HOSTS`
3. Use PostgreSQL instead of SQLite
4. Collect static files: `python manage.py collectstatic`
5. Use Gunicorn: `gunicorn config.wsgi:application`

### Web Frontend Deployment
1. Build production bundle: `npm run build`
2. Deploy to Vercel, Netlify, or serve with Nginx

## Troubleshooting

### Backend Issues
- **Migration errors**: Delete db.sqlite3 and migrations, run makemigrations again
- **Port already in use**: Change port with `python manage.py runserver 8001`
- **CORS errors**: Check CORS_ALLOWED_ORIGINS in settings.py

### Frontend Issues
- **API connection failed**: Verify backend is running and URL is correct
- **Module not found**: Run `npm install` again
- **Build errors**: Clear node_modules and reinstall

## Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit Pull Request

## License

MIT License - Free to use for educational and commercial purposes

## Contact & Support

For questions or issues:
- Create GitHub issue
- Email: [your-email]
- Demo Video: [link-to-video]

## Acknowledgments

- FOSSEE (Free/Libre and Open Source Software for Education)
- IIT Bombay
- Django & React communities

---

**Built with ❤️ for FOSSEE Semester-long Internship Screening Task**