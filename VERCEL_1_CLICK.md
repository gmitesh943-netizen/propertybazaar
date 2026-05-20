# Vercel LIVE — tamne 1 minute (permission)

Hu tamari screen par login nathi kari shaktu. **Ek vaar** aa karo, pachhi badhu automatic:

---

## Option A — Script (recommended)

1. https://vercel.com/account/tokens → **Create Token** → copy
2. Project folder ma **`deploy-vercel.ps1`** right-click → **Run with PowerShell**
3. Token paste karo → Enter
4. 3–5 min pachi Vercel dashboard par URL

**Pehla Vercel dashboard → Project → Settings → Environment Variables:**

| Key | Value |
|-----|--------|
| DATABASE_URL | Neon.tech thi postgres URL |
| DEBUG | False |
| SECRET_KEY | koi pan lambi string |

---

## Option B — Browser (token vagar)

1. https://vercel.com/new/clone?repository-url=https://github.com/gmitesh943-netizen/propertybazaar
2. GitHub login → Deploy
3. Upar 3 environment variables add karo

---

## Render (hve j LIVE — Vercel vagar)

https://propertybazaar.onrender.com  
(30 sec loading = normal)
