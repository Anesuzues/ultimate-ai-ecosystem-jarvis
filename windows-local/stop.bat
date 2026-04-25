@echo off
REM Stop JARVIS dev processes by window title
taskkill /FI "WINDOWTITLE eq JARVIS-MongoDB*" /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq JARVIS-Backend*" /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq JARVIS-Frontend*" /F >nul 2>&1
echo Stopped JARVIS processes.
