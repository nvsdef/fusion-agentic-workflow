@echo off
"%LOCALAPPDATA%\hermes\hermes-agent\venv\Scripts\python.exe" "%~dp0hermes_skill_editor.py" "%~1"
exit /b %errorlevel%
