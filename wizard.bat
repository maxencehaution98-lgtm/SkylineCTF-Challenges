@echo off
setlocal

REM Check if image exists or if --build is passed
docker image inspect skyline-wizard >nul 2>&1
if %ERRORLEVEL% NEQ 0 goto build
if "%1"=="--build" goto build
goto run

:build
echo 🏗️  Construction de l'image Docker du wizard...
docker build -t skyline-wizard -f Dockerfile.wizard .
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Erreur lors de la construction de l'image.
    pause
    exit /b %ERRORLEVEL%
)

:run
echo 🧙‍♂️  Lancement du Wizard...
docker run -it --rm -e PYTHONDONTWRITEBYTECODE=1 -v "%cd%:/app" skyline-wizard

endlocal
