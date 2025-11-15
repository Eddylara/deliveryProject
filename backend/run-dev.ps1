# Run development server for Sabor y Mar Cartagena backend
# Usage: PowerShell -> ./run-dev.ps1

param()

$root = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $root

if (-not (Test-Path -Path .venv)) {
    Write-Host "Creando entorno virtual .venv..."
    python -m venv .venv
}

Write-Host "Activando entorno virtual..."
. .venv\Scripts\Activate.ps1

Write-Host "Instalando dependencias (requirements.txt)..."
pip install -r requirements.txt

Write-Host "Iniciando Uvicorn en http://127.0.0.1:8000 ..."
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
