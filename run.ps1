# Run the Mini_System main flow with a prompted goal

# Resolve paths relative to this script
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$pythonExe = Join-Path $root ".venv\Scripts\python.exe"

if (-not (Test-Path $pythonExe)) {
    $pythonExe = "python"
}

# Prompt for input goal
$goal = Read-Host "Goal"
if ([string]::IsNullOrWhiteSpace($goal)) {
    Write-Host "No goal entered. Exiting."
    exit 1
}

# Run single cycle (default LLM provider is stub)
& $pythonExe -m mini_system.main --goal "$goal"
