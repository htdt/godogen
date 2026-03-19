# Publish godogen skills into a target project directory.
# Creates .claude/skills/ and copies a CLAUDE.md.
#
# Usage: .\publish.ps1 <target_dir> [claude_md]
#   claude_md  Path to CLAUDE.md to use (default: teleforge.md)

param(
    [Parameter(Mandatory=$true)][string]$TargetDir,
    [string]$ClaudeMd
)

$ErrorActionPreference = 'Stop'

$RepoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path

if (-not $ClaudeMd) {
    $ClaudeMd = Join-Path $RepoRoot 'teleforge.md'
}

if (Test-Path $TargetDir) {
    $Target = (Resolve-Path $TargetDir).Path
} else {
    New-Item -ItemType Directory -Path $TargetDir -Force | Out-Null
    $Target = (Resolve-Path $TargetDir).Path
}

Write-Host "Publishing to: $Target"

Remove-Item -Recurse -Force $Target
New-Item -ItemType Directory -Path "$Target\.claude\skills" -Force | Out-Null

$SkillsSrc = Join-Path $RepoRoot 'skills'
Get-ChildItem -Path $SkillsSrc -Recurse |
    Where-Object { $_.FullName -notmatch '\\doc_source' -and $_.FullName -notmatch '\\__pycache__' } |
    ForEach-Object {
        $rel  = $_.FullName.Substring($SkillsSrc.Length + 1)
        $dest = Join-Path "$Target\.claude\skills" $rel
        if ($_.PSIsContainer) {
            New-Item -ItemType Directory -Path $dest -Force | Out-Null
        } else {
            New-Item -ItemType Directory -Path (Split-Path $dest) -Force | Out-Null
            Copy-Item -Path $_.FullName -Destination $dest -Force
        }
    }

Copy-Item -Path $ClaudeMd -Destination "$Target\CLAUDE.md" -Force
Write-Host "Created CLAUDE.md (from $ClaudeMd)"

$gitignore = "$Target\.gitignore"
if (-not (Test-Path $gitignore)) {
    @"
.claude
CLAUDE.md
assets
screenshots
.godot
*.import
"@ | Set-Content $gitignore -Encoding UTF8
    Write-Host "Created .gitignore"
}

git -C $Target init -q 2>$null

$count = (Get-ChildItem "$Target\.claude\skills").Count
Write-Host "Done. skills: $count"
