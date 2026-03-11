$sLinkFile = "$env:USERPROFILE\Desktop\Project-Readiness-Checker.lnk" 
$sTargetFile = "$PSScriptRoot\run_app.bat" 
$sIconFile = "$PSScriptRoot\assets\icon.ico" 
$WshShell = New-Object -ComObject WScript.Shell 
$Shortcut = $WshShell.CreateShortcut($sLinkFile) 
$Shortcut.TargetPath = "cmd.exe"
$Shortcut.Arguments = "/c `"$sTargetFile`""
if (Test-Path $sIconFile) {
    $Shortcut.IconLocation = $sIconFile
} else {
    $Shortcut.IconLocation = "C:\Windows\System32\shell32.dll, 161"
}
$Shortcut.WorkingDirectory = $PSScriptRoot 
$Shortcut.Save()

Write-Host "[RS] Acceso directo creado en el escritorio: Project Readiness Checker" -ForegroundColor Cyan
