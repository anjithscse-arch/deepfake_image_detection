$env:FLASK_DEBUG = "0"
Set-Location $PSScriptRoot

if (Test-Path ".\.venv\Scripts\python.exe") {
    & ".\.venv\Scripts\python.exe" "app.py"
} else {
    python "app.py"
}
