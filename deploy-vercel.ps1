# Vercel par automatic deploy — ek vaar token joiye
# Token: https://vercel.com/account/tokens → Create Token → copy

$ProjectRoot = $PSScriptRoot
Set-Location $ProjectRoot

$tokenFile = Join-Path $ProjectRoot ".vercel-token"
$token = $env:VERCEL_TOKEN
if (-not $token -and (Test-Path $tokenFile)) {
    $token = (Get-Content $tokenFile -Raw).Trim()
}

if (-not $token) {
    Write-Host ""
    Write-Host "VERCEL TOKEN joiye (ek vaar):" -ForegroundColor Yellow
    Write-Host "1. https://vercel.com/account/tokens" -ForegroundColor Cyan
    Write-Host "2. Create Token -> copy" -ForegroundColor Cyan
    Write-Host "3. Token niche paste karo (Enter):" -ForegroundColor Cyan
    $token = Read-Host "Vercel Token"
    if ($token) {
        $token | Set-Content $tokenFile -NoNewline
        Write-Host "Token save thayo: .vercel-token" -ForegroundColor Green
    }
}

if (-not $token) {
    Write-Host "Token vagar deploy nathi thay. Browser thi:" -ForegroundColor Red
    Start-Process "https://vercel.com/new/clone?repository-url=https://github.com/gmitesh943-netizen/propertybazaar"
    exit 1
}

Write-Host "Deploying to Vercel (2-5 min)..." -ForegroundColor Cyan
npx --yes vercel@latest deploy --prod --yes --token $token 2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "SUCCESS! URL check: https://vercel.com/dashboard" -ForegroundColor Green
} else {
    Write-Host "Deploy fail — Vercel dashboard ma Environment Variables add karo:" -ForegroundColor Yellow
    Write-Host "  DATABASE_URL = Neon postgres URL (https://neon.tech)" -ForegroundColor Yellow
    Write-Host "  DEBUG = False" -ForegroundColor Yellow
    Write-Host "  SECRET_KEY = random string" -ForegroundColor Yellow
}
