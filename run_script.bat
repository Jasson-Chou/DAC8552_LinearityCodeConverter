@echo off
setlocal

REM 取得當下批次檔所在目錄
set SCRIPT_DIR=%~dp0

REM 執行 Python 檔案
"C:\...\Python\Python.exe" "%SCRIPT_DIR%dac_converter.py"

endlocal

echo Script Run Done
pause
