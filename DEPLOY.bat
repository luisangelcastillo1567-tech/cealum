@echo off
echo ============================================
echo   CAELUM - Deploy to Netlify via GitHub
echo ============================================
echo.
cd /d "C:\Users\luisa\Downloads\cealum"
echo Staging all files...
git add index.html welcome.html blueprint.html ai-agency-blueprint-3d.html assistant.html dashboard.html admin.html
echo.
echo Committing...
git commit -m "Full site wired — Ollama AI, fixed nav, all products fully functional"
echo.
echo Pushing to GitHub (auto-deploys to Netlify)...
git push
echo.
echo ============================================
echo   Done! Netlify will deploy in ~30 seconds.
echo   Visit: https://caelu.netlify.app
echo ============================================
echo.
pause
