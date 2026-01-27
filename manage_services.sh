#!/bin/bash
# ASC Dashboard Service Management Script

SERVICE_BACKEND="asc-dashboard-backend.service"
SERVICE_FRONTEND="asc-dashboard-frontend.service"

case "$1" in
    start)
        echo "Starting ASC Dashboard services..."
        sudo systemctl start $SERVICE_BACKEND
        sudo systemctl start $SERVICE_FRONTEND
        echo "Services started!"
        ;;
    stop)
        echo "Stopping ASC Dashboard services..."
        sudo systemctl stop $SERVICE_BACKEND
        sudo systemctl stop $SERVICE_FRONTEND
        echo "Services stopped!"
        ;;
    restart)
        echo "Restarting ASC Dashboard services..."
        sudo systemctl restart $SERVICE_BACKEND
        sudo systemctl restart $SERVICE_FRONTEND
        echo "Services restarted!"
        ;;
    status)
        echo "=== Backend Status ==="
        sudo systemctl status $SERVICE_BACKEND --no-pager -l
        echo ""
        echo "=== Frontend Status ==="
        sudo systemctl status $SERVICE_FRONTEND --no-pager -l
        ;;
    logs-backend)
        echo "=== Backend Logs (last 50 lines) ==="
        tail -n 50 /home/ubuntu/ASC-Project-Entry-Exit-Dashboard/logs/backend.log
        echo ""
        echo "=== Backend Error Logs (last 50 lines) ==="
        tail -n 50 /home/ubuntu/ASC-Project-Entry-Exit-Dashboard/logs/backend.error.log
        ;;
    logs-frontend)
        echo "=== Frontend Logs (last 50 lines) ==="
        tail -n 50 /home/ubuntu/ASC-Project-Entry-Exit-Dashboard/logs/frontend.log
        echo ""
        echo "=== Frontend Error Logs (last 50 lines) ==="
        tail -n 50 /home/ubuntu/ASC-Project-Entry-Exit-Dashboard/logs/frontend.error.log
        ;;
    logs)
        echo "=== Backend Logs (last 20 lines) ==="
        tail -n 20 /home/ubuntu/ASC-Project-Entry-Exit-Dashboard/logs/backend.log
        echo ""
        echo "=== Frontend Logs (last 20 lines) ==="
        tail -n 20 /home/ubuntu/ASC-Project-Entry-Exit-Dashboard/logs/frontend.log
        ;;
    follow-backend)
        echo "Following backend logs (Ctrl+C to exit)..."
        tail -f /home/ubuntu/ASC-Project-Entry-Exit-Dashboard/logs/backend.log
        ;;
    follow-frontend)
        echo "Following frontend logs (Ctrl+C to exit)..."
        tail -f /home/ubuntu/ASC-Project-Entry-Exit-Dashboard/logs/frontend.log
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status|logs|logs-backend|logs-frontend|follow-backend|follow-frontend}"
        echo ""
        echo "Commands:"
        echo "  start           - Start both services"
        echo "  stop            - Stop both services"
        echo "  restart         - Restart both services"
        echo "  status          - Show status of both services"
        echo "  logs            - Show recent logs from both services"
        echo "  logs-backend    - Show recent backend logs"
        echo "  logs-frontend   - Show recent frontend logs"
        echo "  follow-backend  - Follow backend logs in real-time"
        echo "  follow-frontend - Follow frontend logs in real-time"
        exit 1
        ;;
esac

exit 0




