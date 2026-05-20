# Step B — Render par live URL (Gujarati)

**Pehla Step A (GitHub) jaruri che.** Repo GitHub par nathi to Step B kaam nathi kare.

---

## Step A — 2 minute (ek vaar)

1. https://github.com → Login
2. Green button **New** → Repository name: `propertybazaar` → **Create repository**
3. Page par **"uploading an existing file"** link
4. Tamara folder `PropertyBazaar_Pytn - Copy` mathi files drag karo  
   **NA upload karo:** `venv` folder, `.env` file, `db.sqlite3`, `media` folder
5. Nichhe **Commit changes** dabavo
6. Repo URL note karo, jem ke:  
   `https://github.com/TAMARU_USERNAME/propertybazaar`

---

## Step B — Render (live URL)

### 1. Account
- Browser: https://dashboard.render.com/register
- **Sign Up with GitHub** (saru — repo automatic dekhashe)
- GitHub permission **Allow** karo

### 2. Blueprint deploy
- Render dashboard: https://dashboard.render.com
- Upar right: **New +** button
- **Blueprint** select karo (Web Service nathi — Blueprint!)

### 3. Repo connect
- **Connect account** (GitHub) jo puchhe to connect karo
- List ma **`propertybazaar`** repo select karo
- **Connect**

### 4. Blueprint review
- Render `render.yaml` file read karse
- Service name: `propertybazaar` dekhashe
- **Apply** dabavo

### 5. Wait
- **Logs** tab kholo
- 5–15 minute wait (Build → Deploy)
- Success: **Live** green badge

### 6. Tamaro URL
- Dashboard → **propertybazaar** service → uper URL  
  Example: `https://propertybazaar.onrender.com`  
  (name thi thodu alag hoi shake)

Aa URL **permanent** che (free tier par site 15 min unused pachi slow wake thay).

---

## Deploy pachi (optional)

### Admin login banavva
Render → propertybazaar → **Shell** tab:
```bash
python manage.py createsuperuser
```
Pachhi: `https://TAMARU-URL.onrender.com/admin/`

### Database permanent (data save — Neon free)
1. https://neon.tech → project → connection string copy
2. Render → propertybazaar → **Environment** → Add Variable:
   - `DATABASE_URL` = neon no string
3. **Manual Deploy** → Deploy latest commit

---

## Error aave to

| Problem | Solution |
|---------|----------|
| Repo list ma nathi | GitHub par code upload karo (Step A) |
| Build failed | Logs screenshot — `collectstatic` / `migrate` error |
| 400 Bad Request | Environment ma `ALLOWED_HOSTS` = tamaro Render URL (comma vagar) |
| Site slow | Free tier sleep — normal |

---

## Quick links

- Render login: https://dashboard.render.com
- New Blueprint: https://dashboard.render.com/blueprints/new
- GitHub new repo: https://github.com/new
