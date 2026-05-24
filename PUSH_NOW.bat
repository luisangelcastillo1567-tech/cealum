@echo off
echo Pushing all updates to Netlify...
cd /d "C:\Users\luisa\Downloads\cealum"
git add shop.html index.html welcome.html blueprint.html assistant.html dashboard.html ai-agency-blueprint-3d.html
git commit -m "Add Shop page + Shop nav link on all pages"
git push
echo.
echo Done! Live in ~30 seconds at https://caelu.netlify.app
echo.
pause
