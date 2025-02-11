@echo off
REM Create the directory if it doesn't exist
if not exist "C:\chrome\1010" mkdir "C:\chrome\1010"

start chrome.exe -remote-debugging-port=1010 --user-data-dir="C:\chrome\1010"

pause