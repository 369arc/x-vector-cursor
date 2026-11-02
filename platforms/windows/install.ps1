param(
    [ValidateSet('X-Vector', 'X-Vector-Inverse')]
    [string]$Variant = 'X-Vector',
    [switch]$Uninstall
)

$ErrorActionPreference = 'Stop'

$root = Join-Path $env:LOCALAPPDATA 'X-Vector'
$dest = Join-Path $root 'Cursors'
$key = 'HKCU:\Control Panel\Cursors'
$roles = @(
    'Arrow', 'Help', 'AppStarting', 'Wait', 'Crosshair', 'IBeam',
    'No', 'Hand', 'Pin', 'Person', 'Link', 'SizeAll'
)

function Update-Cursors {
    if (-not ('XVectorCursors' -as [type])) {
        Add-Type @"
using System;
using System.Runtime.InteropServices;
public static class XVectorCursors {
    [DllImport("user32.dll", SetLastError = true)]
    public static extern bool SystemParametersInfo(uint uiAction, uint uiParam, IntPtr pvParam, uint fWinIni);
}
"@
    }
    [XVectorCursors]::SystemParametersInfo(0x0057, 0, [IntPtr]::Zero, 0x0003) | Out-Null
}

if ($Uninstall) {
    New-Item -Path $key -Force | Out-Null
    foreach ($role in $roles) {
        Remove-ItemProperty -Path $key -Name $role -ErrorAction SilentlyContinue
    }
    Set-Item -Path $key -Value 'Windows Default'
    if (Test-Path $root) {
        Remove-Item -Path $root -Recurse -Force
    }
    Update-Cursors
    Write-Host 'X-Vector removed. Select another scheme in Mouse Properties if needed.'
    exit 0
}

$source = Join-Path $PSScriptRoot $Variant
if (-not (Test-Path $source)) {
    throw "Variant folder not found: $source"
}

New-Item -Path $key -Force | Out-Null
New-Item -ItemType Directory -Force -Path $dest | Out-Null
Copy-Item -Path (Join-Path $source '*.cur') -Destination $dest -Force

$map = [ordered]@{
    'Arrow'       = 'default.cur'
    'Help'        = 'default.cur'
    'AppStarting' = 'default.cur'
    'Wait'        = 'default.cur'
    'Crosshair'   = 'default.cur'
    'IBeam'       = 'text.cur'
    'No'          = 'not-allowed.cur'
    'Hand'        = 'default.cur'
    'Pin'         = 'default.cur'
    'Person'      = 'default.cur'
    'Link'        = 'default.cur'
    'SizeAll'     = 'default.cur'
}

foreach ($role in $map.Keys) {
    Set-ItemProperty -Path $key -Name $role -Value (Join-Path $dest $map[$role]) -Type ExpandString
}
Set-Item -Path $key -Value $Variant
Update-Cursors

Write-Host "X-Vector ($Variant) applied from $dest"
Write-Host 'Resize cursors stay native. Open Mouse Properties to fine-tune.'
