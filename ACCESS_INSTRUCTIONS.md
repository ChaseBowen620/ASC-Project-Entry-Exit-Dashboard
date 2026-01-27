# Accessing the ASC Dashboard

## Access the Dashboard

The dashboard is available at:

**https://ascprojectsurvey.com**

## If you see "Connection is not secure" or certificate errors

If you see certificate or connection errors:

1. **Clear your browser cache** for this site
2. **Ensure you're using https://** (not http://): `https://ascprojectsurvey.com`
3. If your browser has cached security policies, you can:
   - Clear the HSTS (HTTP Strict Transport Security) cache for this domain

## Browser-specific instructions

### Chrome/Edge
1. Type `chrome://net-internals/#hsts` in the address bar
2. Under "Delete domain security policies", enter `ascprojectsurvey.com`
3. Click "Delete"
4. Try accessing `https://ascprojectsurvey.com` again

### Firefox
1. Clear site data: Settings → Privacy & Security → Cookies and Site Data → Clear Data
2. Or use Private/Incognito mode to test

### Safari
1. Clear browsing data: Safari → Clear History
2. Or use Private mode

## Current Setup

- **Frontend**: Accessible via nginx at https://ascprojectsurvey.com
- **Backend API**: Accessible at https://ascprojectsurvey.com/api/
- **Direct access** (development only, if nginx is bypassed):
  - Frontend: `http://localhost:3000`
  - Backend: `http://localhost:8000/api/`

## HTTPS / SSL (Certbot + nginx)

HTTPS is provided by **Let's Encrypt** via **Certbot**. To set it up on the server:

### Prerequisites

- **DNS**: `ascprojectsurvey.com` must point to this server’s public IP.
- **nginx** installed; ports **80** and **443** open in the firewall/security group.
- **Django and React** running (`localhost:8000`, `localhost:3000`) if the site should work during setup.

### One-time setup

From the project root, run:

```bash
sudo ./setup_https_certbot.sh
```

For expiration notices, set your email:

```bash
sudo CERTBOT_EMAIL=you@example.com ./setup_https_certbot.sh
```

The script will:

1. Install Certbot (if needed)
2. Use a temporary HTTP-only nginx config so Let's Encrypt can validate the domain
3. Request a certificate for `ascprojectsurvey.com`
4. Deploy the final nginx config with HTTPS and an HTTP→HTTPS redirect

### Renewal

Certbot typically installs a systemd timer or cron for renewal. Test it with:

```bash
sudo certbot renew --dry-run
```

To reload nginx after each renewal, you can add a deploy hook or run:

```bash
sudo certbot renew --deploy-hook "systemctl reload nginx"
```
