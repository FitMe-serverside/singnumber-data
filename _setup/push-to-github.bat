@echo off
setlocal
cd /d "%~dp0.."
if not exist ".github\workflows" mkdir ".github\workflows"
copy /y "_setup\daily.yml" ".github\workflows\daily.yml" >nul
echo [1/3] workflow file placed at .github\workflows\daily.yml
where git >nul 2>nul
if errorlevel 1 (
  echo [!] git is not installed. Install Git for Windows, then run this again.
  echo     https://git-scm.com/download/win
  pause
  exit /b 1
)
if not exist ".git" (
  git init -b main
  git config user.name "SingNumber"
  git config user.email "postshare.co.kr@gmail.com"
  git config core.autocrlf false
  git add .
  git commit -m "init data feed"
  echo [2/3] local repository created
) else (
  git config user.name "SingNumber"
  git config user.email "postshare.co.kr@gmail.com"
  git config core.autocrlf false
  git add .
  git commit -m "update data feed" 
  echo [2/3] changes committed
)
git remote get-url origin >nul 2>nul
if errorlevel 1 git remote add origin https://github.com/FitMe-serverside/singnumber-data.git
echo [3/3] pushing to GitHub (a browser login window may open)...
git push -u origin main
if errorlevel 1 echo PUSH FAILED - see message above
echo.
echo DONE. Next: GitHub repo Settings ^> Actions ^> General ^> Workflow permissions ^> "Read and write"
pause
