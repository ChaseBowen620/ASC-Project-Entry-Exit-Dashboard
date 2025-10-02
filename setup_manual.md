# Manual Setup with uv

If you prefer to set up the dashboard manually using `uv`, follow these steps:

## Prerequisites
- Python 3.8+ installed
- Node.js and npm installed
- `uv` installed: `pip install uv`

## Step-by-Step Setup

### 1. Create Virtual Environment
```bash
uv venv
```

### 2. Activate Virtual Environment
```bash
# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

### 3. Install Python Dependencies
```bash
uv pip install -r requirements.txt
```

### 4. Set Up Django Database
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Import Survey Data
```bash
python manage.py import_survey_data "ASC Project Survey_September 19, 2025_15.07.csv"
```

### 6. Install React Dependencies
```bash
cd frontend
npm install
cd ..
```

### 7. Start the Application

**Terminal 1 - Django Backend:**
```bash
# Make sure virtual environment is activated
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # macOS/Linux

python manage.py runserver
```

**Terminal 2 - React Frontend:**
```bash
cd frontend
npm start
```

## Access Points
- **React Dashboard**: http://localhost:3000
- **Django API**: http://localhost:8000/api/
- **Django Admin**: http://localhost:8000/admin/

## Troubleshooting

### Virtual Environment Issues
- Make sure `uv` is installed: `pip install uv`
- If activation fails, try: `uv venv --force` to recreate the environment

### Django Issues
- Ensure virtual environment is activated before running Django commands
- Check that all dependencies are installed: `uv pip list`

### React Issues
- Make sure you're in the `frontend` directory when running `npm` commands
- Try deleting `node_modules` and running `npm install` again

