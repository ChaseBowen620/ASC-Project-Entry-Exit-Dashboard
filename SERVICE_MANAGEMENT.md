# ASC Dashboard Service Management

Your frontend and backend are now running as systemd services, which means they will:
- ✅ Start automatically when the server boots
- ✅ Restart automatically if they crash
- ✅ Run in the background continuously
- ✅ Log all output to files

## Quick Commands

Use the management script for easy control:

```bash
cd /home/ubuntu/ASC-Project-Entry-Exit-Dashboard

# Check status
./manage_services.sh status

# Restart both services
./manage_services.sh restart

# Stop both services
./manage_services.sh stop

# Start both services
./manage_services.sh start

# View recent logs
./manage_services.sh logs

# View backend logs only
./manage_services.sh logs-backend

# View frontend logs only
./manage_services.sh logs-frontend

# Follow logs in real-time
./manage_services.sh follow-backend
./manage_services.sh follow-frontend
```

## Direct systemctl Commands

You can also use systemctl directly:

```bash
# Check status
sudo systemctl status asc-dashboard-backend.service
sudo systemctl status asc-dashboard-frontend.service

# Restart a service
sudo systemctl restart asc-dashboard-backend.service
sudo systemctl restart asc-dashboard-frontend.service

# Stop a service
sudo systemctl stop asc-dashboard-backend.service
sudo systemctl stop asc-dashboard-frontend.service

# Start a service
sudo systemctl start asc-dashboard-backend.service
sudo systemctl start asc-dashboard-frontend.service

# View logs (last 100 lines)
sudo journalctl -u asc-dashboard-backend.service -n 100
sudo journalctl -u asc-dashboard-frontend.service -n 100

# Follow logs in real-time
sudo journalctl -u asc-dashboard-backend.service -f
sudo journalctl -u asc-dashboard-frontend.service -f
```

## Log Files

Logs are also written to files:
- Backend: `/home/ubuntu/ASC-Project-Entry-Exit-Dashboard/logs/backend.log`
- Backend Errors: `/home/ubuntu/ASC-Project-Entry-Exit-Dashboard/logs/backend.error.log`
- Frontend: `/home/ubuntu/ASC-Project-Entry-Exit-Dashboard/logs/frontend.log`
- Frontend Errors: `/home/ubuntu/ASC-Project-Entry-Exit-Dashboard/logs/frontend.error.log`

## Service Status

Both services are configured to:
- **Auto-start on boot**: Enabled
- **Auto-restart on failure**: Enabled (restarts after 10 seconds)
- **Run as user**: `ubuntu`
- **Backend port**: `8000`
- **Frontend port**: `3000`

## Troubleshooting

If a service fails to start:
1. Check the status: `sudo systemctl status asc-dashboard-backend.service`
2. Check the logs: `./manage_services.sh logs-backend`
3. Check for port conflicts: `sudo netstat -tulpn | grep -E '8000|3000'`
4. Verify environment variables are set in `.env` files

## Disabling Auto-Start

If you want to disable auto-start on boot:
```bash
sudo systemctl disable asc-dashboard-backend.service
sudo systemctl disable asc-dashboard-frontend.service
```

To re-enable:
```bash
sudo systemctl enable asc-dashboard-backend.service
sudo systemctl enable asc-dashboard-frontend.service
```




