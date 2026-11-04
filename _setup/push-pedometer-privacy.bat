@echo off
setlocal
cd /d "%~dp0.."
set "LOG=%~dp0push-pedometer.log"
echo [%date% %time%] start > "%LOG%"
git config user.name "SingNumber"
git config user.email "postshare.co.kr@gmail.com"
git config core.autocrlf false
git add docs\pedometer-privacy.html _setup\push-pedometer-privacy.bat >> "%LOG%" 2>&1
git commit -m "add pedometer privacy policy" >> "%LOG%" 2>&1
git pull --rebase --autostash origin main >> "%LOG%" 2>&1
git push origin main >> "%LOG%" 2>&1
echo PUSH_EXIT=%errorlevel% >> "%LOG%"
echo [%date% %time%] DONE >> "%LOG%"
exit
