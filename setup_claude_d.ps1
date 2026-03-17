$configDir = "D:\ClaudeCodeConfig"
$sourceFile = "$env:USERPROFILE\.claude.json"
$targetFile = "$configDir\.claude.json"

# Create target directory if it doesn't exist
if (-Not (Test-Path -Path $configDir)) {
    New-Item -ItemType Directory -Force -Path $configDir
    Write-Host "Created directory $configDir"
}

# If the source file exists and is not a symlink, move it
if (Test-Path -Path $sourceFile) {
    if ((Get-Item $sourceFile).LinkType -ne "SymbolicLink") {
        if (Test-Path -Path $targetFile) {
            Write-Host "Target file $targetFile already exists. Archiving old source file."
            Rename-Item -Path $sourceFile -NewName ".claude.json.bak"
        } else {
            Move-Item -Path $sourceFile -Destination $targetFile
            Write-Host "Moved $sourceFile to $targetFile"
        }
    } else {
        Write-Host "$sourceFile is already a symbolic link. Removing old link."
        Remove-Item -Path $sourceFile
    }
}

# Create a symbolic link
New-Item -ItemType SymbolicLink -Path $sourceFile -Target $targetFile
Write-Host "Created symbolic link from $sourceFile to $targetFile"
