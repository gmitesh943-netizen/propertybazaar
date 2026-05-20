# PropertyBazaar — Online host (Gujarati)

Tame keval **3 step** karo. Baaki code ready che.

---

## Step 1: GitHub par code muko (5 minute)

1. Browser ma jao: **https://github.com** → Login / Sign up (free)
2. **New repository** → Name: `propertybazaar` → **Create**
3. GitHub repo page par **"uploading an existing file"** par click karo
4. Tamara folder `PropertyBazaar_Pytn - Copy` mathi **badha files** drag-drop karo  
   **IMPORTANT:** `venv` folder ane `.env` file **upload NATHI karvi**
5. **Commit changes**

---

## Step 2: Render par live site (5 minute)

1. Jao: **https://render.com** → Sign up (GitHub thi login — saru)
2. **New +** → **Blueprint**
3. Tamaru GitHub repo `propertybazaar` select karo
4. Render `render.yaml` file automatic read karse → **Apply**
5. 5–10 minute wait → **Live URL** malse:  
   `https://propertybazaar-xxxx.onrender.com`

---

## Step 3 (optional): Database permanent (Neon — free)

Bina database site chale, pan data restart pachi gay thai shake.

1. **https://neon.tech** → free account → **Create project**
2. **Connection string** copy karo (`postgresql://...`)
3. Render dashboard → tamari service → **Environment** → add:
   - `DATABASE_URL` = (Neon no string)
   - `ALLOWED_HOSTS` = `propertybazaar-xxxx.onrender.com` (tamaro Render URL)
   - `CSRF_TRUSTED_ORIGINS` = `https://propertybazaar-xxxx.onrender.com`
4. **Manual Deploy** → **Deploy latest commit**

Admin user banavva mate Render **Shell** ma:
```bash
python manage.py createsuperuser
```

---

## Turant URL (account vagar — demo mate)

Project folder ma `start-public-url.ps1` double-click karo.  
Internet par temporary link malse (PC band = link band).

---

## Madad

Koi error aave to Render → **Logs** tab screenshot moklo.
