#!/bin/bash
echo "Building and starting ASC Survey Dashboard..."
echo ""

cd /home/ubuntu/ASC-Project-Entry-Exit-Dashboard

# Build the React frontend
echo "Building React frontend..."
cd frontend
npm run build
if [ $? -ne 0 ]; then
    echo "Frontend build failed!"
    exit 1
fi
cd ..

echo ""
echo "Build complete! Starting services..."
echo ""

# Start the dashboard
./start_dashboard.sh



