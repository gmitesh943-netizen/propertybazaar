# Render — Blueprint black screen? Web Service thi deploy

Blueprint page khali/black aave to **aa rite** karo:

## 1. Web Service (Blueprint vagar)

1. https://dashboard.render.com
2. Upar **+ New** → **Web Service** (Blueprint NATHI)
3. **Connect GitHub** → repo: `gmitesh943-netizen/propertybazaar`
4. Form bharno:

| Field | Value |
|-------|--------|
| Name | `propertybazaar` |
| Region | Singapore (or closest) |
| Branch | `main` |
| Runtime | **Python 3** |
| Build Command | `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate --noinput` |
| Start Command | `gunicorn config.wsgi:application --bind 0.0.0.0:$PORT` |
| Instance Type | **Free** |

5. **Environment Variables** (Add):

| Key | Value |
|-----|--------|
| DEBUG | False |
| PYTHON_VERSION | 3.12.8 |

(SECRET_KEY Render auto generate kari shake — ke manually random string)

6. **Create Web Service** → wait 5–15 min
7. URL: service page par `https://propertybazaar.onrender.com`

## 2. Blueprint page fix try karo

- Page **Refresh** (F5)
- **Chrome / Edge** try karo
- **Incognito** window
- Ad-blocker band karo
- VPN band karo

## 3. GitHub connect

Render → Account Settings → GitHub → **Connect**  
Repo `propertybazaar` access **Allow**
