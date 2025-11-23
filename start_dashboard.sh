#!/bin/bash
echo "Starting ASC Survey Dashboard..."
echo ""

# Kill any existing processes on ports 8000 and 3000
echo "Stopping any existing processes..."
pkill -f "python manage.py runserver" 2>/dev/null
pkill -f "react-scripts start" 2>/dev/null
sleep 2

echo "Starting Django Backend..."
cd /home/ubuntu/ASC-Project-Entry-Exit-Dashboard
cd backend
nohup /home/ubuntu/ASC-Project-Entry-Exit-Dashboard/.venv/bin/python manage.py runserver 0.0.0.0:8000 > ../nohup_backend.out 2>&1 &
BACKEND_PID=$!
echo "Backend started (PID: $BACKEND_PID)"

echo "Waiting 5 seconds for Django to start..."
sleep 5

echo "Starting React Frontend..."
cd ../frontend
nohup npm start > ../nohup_frontend.out 2>&1 &
FRONTEND_PID=$!
echo "Frontend started (PID: $FRONTEND_PID)"

echo ""
echo "Dashboard is starting up!"
echo "Django Backend: http://18.144.20.248:8000"
echo "React Frontend: http://18.144.20.248:3000"
echo ""
echo "Backend logs: tail -f /home/ubuntu/ASC-Project-Entry-Exit-Dashboard/nohup_backend.out"
echo "Frontend logs: tail -f /home/ubuntu/ASC-Project-Entry-Exit-Dashboard/nohup_frontend.out"
echo ""
echo "To stop: pkill -f 'python manage.py runserver' && pkill -f 'react-scripts start'"

