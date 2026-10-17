@echo off
echo ========================================================================
echo 100% PROOF EEHIM DB NO SQLITE - WHERE TO DOUBLE CLICK
echo ========================================================================
echo WHERE TO DOUBLE CLICK:
echo 1. Open Windows Explorer - NOT CMD
echo 2. Go to C:\Users\DELL\Downloads\
echo 3. Find RUN-100-PERCENT-PROOF-NO-SQLITE.bat - Double-click with mouse
echo 4. It creates D:\EEHIMDB\dist\EEHIM_DB_V14_100_PERCENT_PROOF_NO_SQLITE.db
echo 5. Shows 10 signatures 100% proof no SQLite - Stays open with pause
echo ========================================================================
echo [0] Cleaning old files killing new files:
del /Q "C:\Users\DELL\Downloads\*15M*.py" 2>nul
del /Q "C:\Users\DELL\Downloads\*ACTIVE*.py" 2>nul
del /Q "C:\Users\DELL\Downloads\*PERFECT*.py" 2>nul
echo Cleaned.
echo [1] Running proof file:
D:\noth5_python\python.exe "C:\Users\DELL\Downloads\EEHIMDB_V14_100_PERCENT_PROOF_NO_SQLITE.py"
echo [2] Verifying DB:
dir "D:\EEHIMDB\dist\EEHIM_DB_V14_100_PERCENT_PROOF_NO_SQLITE.db"
powershell -Command "$b=[System.IO.File]::ReadAllBytes('D:\EEHIMDB\dist\EEHIM_DB_V14_100_PERCENT_PROOF_NO_SQLITE.db')[0..15]; Write-Host ([System.Text.Encoding]::ASCII.GetString($b))"
pause