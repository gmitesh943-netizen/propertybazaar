# Vercel par PropertyBazaar (Free) — Gujarati

## Important (vanchi lo)

- **Django + Vercel** = possible, pan tamaro project **mota** che (ckeditor, images, payments).
- **Render par site LIVE che** — `https://propertybazaar.onrender.com`
- Vercel par **database (Neon)** jaruri — SQLite kaam nathi kare.
- Photo upload / media Vercel par **limited** che.

---

## Step 1 — Neon database (free, 2 min)

1. https://neon.tech → Sign up
2. **New Project** → connection string copy (`postgresql://...`)
3. Aa string save karo — `DATABASE_URL`

---

## Step 2 — Vercel deploy (3 click)

1. Link open karo:  
   **https://vercel.com/new/clone?repository-url=https://github.com/gmitesh943-netizen/propertybazaar**

   Ke: https://vercel.com/new → **Import** → GitHub → `propertybazaar`

2. **Sign in with GitHub**

3. **Environment Variables** add karo:

| Name | Value |
|------|--------|
| `DATABASE_URL` | Neon no postgres URL |
| `DEBUG` | `False` |
| `SECRET_KEY` | koi pan lambi random string |

4. **Deploy** dabavo → 3–10 min wait

5. URL malse: `https://propertybazaar.vercel.app`  
   (name alag hoi shake: `propertybazaar-xxx.vercel.app`)

---

## Error aave to

| Error | Fix |
|-------|-----|
| Build fail / 250MB | Render use karo (already working) |
| 500 error | `DATABASE_URL` check karo |
| CSRF | Vercel URL `CSRF_TRUSTED_ORIGINS` ma add |

---

## Recommendation

**Portfolio / internship:** Render URL use karo — full Django mate best.  
Vercel = try kari shakay, pan guarantee nathi.
