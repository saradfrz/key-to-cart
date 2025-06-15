<#
.SYNOPSIS
Installs a Python package, updates requirements.txt, stages and commits it to Git.

.DESCRIPTION
This script automates the workflow of:
1. Installing a Python package via pip
2. Freezing dependencies to requirements.txt
3. Adding the file to git
4. Committing with the message "add: <package>"

.PARAMETER PackageName
The name of the Python package to install and commit.

.EXAMPLE
.\install-pkg.ps1 -PackageName flask
#>

param (
    [Parameter(Mandatory = $true)]
    [string]$PackageName
)

# Step 1: Install the package
Write-Host "Installing package '$PackageName'..."
pip install $PackageName

if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to install package '$PackageName'. Aborting."
    exit 1
}

# Step 2: Freeze to requirements.txt
Write-Host "Freezing installed packages to requirements.txt..."
pip freeze > requirements.txt

# Step 3: Git add
Write-Host "Adding requirements.txt to Git staging..."
git add requirements.txt

# Step 4: Git commit
$commitMessage = "install(package): Install $PackageName"
Write-Host "Committing with message: $commitMessage"
git commit -m $commitMessage
