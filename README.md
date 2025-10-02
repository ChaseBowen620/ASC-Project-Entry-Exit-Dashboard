# ASC Survey Dashboard

A complete dashboard application for visualizing ASC (Applied Science Center) survey data from Qualtrics exports.

## Features

### Backend (Django)
- **Survey Data Management**: Store and manage both "starting" and "ending" project survey responses
- **Qualtrics Integration**: Import CSV exports directly from Qualtrics
- **REST API**: Full REST API for frontend consumption
- **Dashboard Analytics**: Pre-built endpoints for dashboard statistics and analytics
- **Admin Interface**: Django admin for data management

### Frontend (React)
- **Color-Coded Summary Metrics**: Visual representation of survey responses with -1 to 1 scale
- **Interactive Dashboard**: Real-time data visualization
- **Responsive Design**: Works on desktop and mobile devices
- **Summary Numbers**: Displays Q3.9, Q3.10, Q3.11, and Q3.12 ratings with color coding

## Quick Start

### Option 1: Automated Setup (Windows with uv)
1. Run `setup_dashboard.bat` to create virtual environment and install dependencies
2. Run `start_dashboard.bat` to start both backend and frontend

### Option 2: Manual Setup with uv

#### Prerequisites
- Python 3.8+ installed
- Node.js and npm installed
- `uv` installed: `pip install uv`

#### Backend Setup
```bash
# Create virtual environment
uv venv

# Activate virtual environment (Windows)
.venv\Scripts\activate

# Install Python dependencies
uv pip install -r requirements.txt

# Set up database
python manage.py makemigrations
python manage.py migrate

# Import survey data
python manage.py import_survey_data "ASC Project Survey_September 19, 2025_15.07.csv"

# Start Django server
python manage.py runserver
```

#### Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start React development server
npm start
```

### Option 3: Manual Setup (Traditional pip)
See `setup_manual.md` for detailed instructions.

## Access Points
- **React Dashboard**: http://localhost:3000
- **Django API**: http://localhost:8000/api/
- **Django Admin**: http://localhost:8000/admin/

## API Endpoints

### Survey Responses
- `GET /api/responses/` - List all survey responses
- `POST /api/responses/` - Create a new survey response
- `GET /api/responses/{id}/` - Get specific survey response
- `PUT /api/responses/{id}/` - Update survey response
- `DELETE /api/responses/{id}/` - Delete survey response

### Data Import
- `POST /api/import/` - Import Qualtrics CSV file

### Dashboard Analytics
- `GET /api/dashboard/stats/` - Get dashboard statistics
- `GET /api/dashboard/analytics/` - Get detailed analytics data

### Survey Choices
- `GET /api/choices/` - Get survey choice mappings

## Data Model

The system handles two types of surveys:

### Starting Project Survey (survey_type = 1)
- Basic project information (A-number, title, mentor)
- Confidence levels and resource assessment
- Learning goals and expectations

### Ending Project Survey (survey_type = 2)
- Project outcomes and learnings
- Skills improvement assessment
- Experience ratings (1-3 scale)
- Recommendation likelihood (1-5 scale)

## Environment Variables

Create a `.env` file with:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
REDIS_URL=redis://localhost:6379/0
```

## Summary Numbers Visualization

The dashboard displays color-coded summary metrics for key survey questions:

### Questions Displayed:
- **Q3.9**: Hard Skills Improved (1-5 scale)
- **Q3.10**: Soft Skills Improved (1-5 scale) 
- **Q3.11**: Confidence in Job Placement (1-5 scale)
- **Q3.12_1-8**: Experience Ratings (1-3 scale)
  - ASC Onboarding
  - Project Initiation
  - Project Mentorship
  - Project Team
  - Project Communications
  - Expectations
  - Project Sponsor/Contact
  - Workload

### Color Coding:
- **Black (0)**: Neutral value
- **Red (-1)**: Negative/poor ratings
- **Green (+1)**: Positive/excellent ratings
- **Gradient**: Intensity based on how far from neutral

### Scale Transformation:
- **1-5 scale** → -1 to +1: `((value - 1) / 4) * 2 - 1`
- **1-3 scale** → -1 to +1: `((value - 1) / 2) * 2 - 1`

## Admin Interface

Access the Django admin at `http://localhost:8000/admin/` to:
- View and manage survey responses
- Add survey choice mappings
- Monitor data quality
