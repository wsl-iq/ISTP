$filesToDelete = @(
    "Android.py",
    "README.md",
    "image.png",
    "install.bat",
    "install.sh",
    "istp.py",
    "requirements.txt",
    "server.py",
    "Linux",
    "MacBook",
    "Windows",
    "server"
)

foreach ($file in $filesToDelete) {
    if (Test-Path $file) {
        Remove-Item $file -Force
        Write-Host "Deleted file: $file"
    } else {
        Write-Host "File $file not found."
    }
}

$scriptPath = $MyInvocation.MyCommand.Path
if (Test-Path $scriptPath) {
    Remove-Item $scriptPath -Force
    Write-Host "Deleted the script itself: $scriptPath"
}
