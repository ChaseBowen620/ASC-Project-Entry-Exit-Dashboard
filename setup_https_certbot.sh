#!/bin/bash
# setup_https_certbot.sh – obtain Let's Encrypt HTTPS cert with Certbot and enable HTTPS in nginx
#
# Prerequisites:
#   - ascprojectsurvey.com DNS points to this server's public IP
#   - nginx installed; ports 80 and 443 open
#   - Django and React are running (localhost:8000, localhost:3000) if you want the site up during setup
#
# Usage:
#   sudo ./setup_https_certbot.sh
#   # Or with email for Let's Encrypt (recommended):
#   sudo CERTBOT_EMAIL=you@example.com ./setup_https_certbot.sh
#
# Renewal: Certbot installs a timer/cron. Test with:
#   sudo certbot renew --dry-run
# To reload nginx after renewal, add a deploy hook or rely on:
#   sudo certbot renew --deploy-hook "systemctl reload nginx"

set -e

if [ "$(id -u)" -ne 0 ]; then
  echo "Run this script with sudo."
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DOMAIN=ascprojectsurvey.com
CERTBOT_ROOT=/var/www/certbot
NGINX_SA=/etc/nginx/sites-available/asc-dashboard
NGINX_SE=/etc/nginx/sites-enabled/asc-dashboard

echo "=== ASC Dashboard – HTTPS setup with Certbot ==="
echo "Domain: $DOMAIN"
echo ""

# If cert already exists, only (re)deploy the HTTPS nginx config
if [ -f /etc/letsencrypt/live/ascprojectsurvey.com/fullchain.pem ]; then
  echo "Certificate already exists. Deploying HTTPS nginx config..."
  cp "$SCRIPT_DIR/nginx-asc-dashboard.conf" "$NGINX_SA"
  nginx -t && systemctl reload nginx
  echo "Done. https://$DOMAIN"
  exit 0
fi

# 1) Install Certbot (Ubuntu/Debian)
if ! command -v certbot &>/dev/null; then
  echo "Installing Certbot..."
  apt-get update -qq
  apt-get install -y certbot
else
  echo "Certbot is already installed."
fi

# 2) Webroot for ACME challenges
echo "Preparing $CERTBOT_ROOT for ACME challenges..."
mkdir -p "$CERTBOT_ROOT"
chown -R www-data:www-data "$CERTBOT_ROOT" 2>/dev/null || true

# 3) Bootstrap: HTTP-only config (proxy + .well-known) so Certbot can validate
echo "Deploying HTTP-only nginx config for certificate issuance..."
cp "$SCRIPT_DIR/nginx-asc-dashboard-bootstrap.conf" "$NGINX_SA"

# 4) Ensure nginx site is enabled
if [ ! -L "$NGINX_SE" ] && [ ! -f "$NGINX_SE" ]; then
  echo "Enabling nginx site asc-dashboard..."
  ln -sf "$NGINX_SA" "$NGINX_SE"
fi

nginx -t
systemctl reload nginx
echo "Nginx reloaded (HTTP only)."

# 5) Obtain certificate (webroot)
CERTBOT_EXTRA=()
if [ -n "$CERTBOT_EMAIL" ]; then
  CERTBOT_EXTRA=(-m "$CERTBOT_EMAIL")
else
  CERTBOT_EXTRA=(--register-unsafely-without-email)
  echo "CERTBOT_EMAIL not set; using --register-unsafely-without-email. Set it for expiration notices."
fi

echo "Requesting certificate from Let's Encrypt for $DOMAIN..."
certbot certonly --webroot -w "$CERTBOT_ROOT" -d "$DOMAIN" --non-interactive --agree-tos "${CERTBOT_EXTRA[@]}"
echo "Certificate obtained."

# 6) Deploy full HTTPS nginx config (HTTP redirect + HTTPS with certificates)
echo "Deploying HTTPS nginx config..."
cp "$SCRIPT_DIR/nginx-asc-dashboard.conf" "$NGINX_SA"
nginx -t
systemctl reload nginx
echo "Nginx reloaded (HTTPS enabled)."

echo ""
echo "=== HTTPS is enabled ==="
echo "  https://$DOMAIN"
echo "  https://$DOMAIN/api/"
echo ""
echo "Renewal: run 'sudo certbot renew --dry-run' to test. Reload nginx after renew if not using a deploy-hook."
