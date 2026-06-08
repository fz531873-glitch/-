param(
    [switch]$NoBackup,
    [switch]$Backup
)

$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$CodexSkills = Join-Path $HOME ".codex\skills"
$Stamp = Get-Date -Format "yyyyMMdd-HHmmss"

$RequiredExisting = @(
    ".codex\skills\paper-spine\SKILL.md",
    ".codex\skills\nature-writing\manifest.yaml",
    ".codex\skills\nature-polishing\manifest.yaml",
    ".codex\skills\docx-editor-cn\SKILL.md"
)

foreach ($Required in $RequiredExisting) {
    $RequiredPath = Join-Path $HOME $Required
    if (-not (Test-Path -LiteralPath $RequiredPath)) {
        throw "Missing prerequisite: $RequiredPath. Install the base PaperSpine/Nature/docx skills before applying hydro-writing-core."
    }
}

$Mappings = @(
    @{
        Source = "skills\hydraulic-writing-router\SKILL.md"
        Target = ".codex\skills\hydraulic-writing-router\SKILL.md"
    },
    @{
        Source = "skills\hydraulic-writing-router\agents\openai.yaml"
        Target = ".codex\skills\hydraulic-writing-router\agents\openai.yaml"
    },
    @{
        Source = "skills\paper-spine\SKILL.md"
        Target = ".codex\skills\paper-spine\SKILL.md"
    },
    @{
        Source = "skills\paper-spine\references\suite-map.md"
        Target = ".codex\skills\paper-spine\references\suite-map.md"
    },
    @{
        Source = "skills\paper-spine\scripts\template_leak_guard.py"
        Target = ".codex\skills\paper-spine\scripts\template_leak_guard.py"
    },
    @{
        Source = "skills\paper-spine\scripts\word_guard.py"
        Target = ".codex\skills\paper-spine\scripts\word_guard.py"
    },
    @{
        Source = "skills\paper-spine-build\SKILL.md"
        Target = ".codex\skills\paper-spine-build\SKILL.md"
    },
    @{
        Source = "skills\paper-spine-build\references\rewrite-matrix.md"
        Target = ".codex\skills\paper-spine-build\references\rewrite-matrix.md"
    },
    @{
        Source = "skills\paper-spine-rewrite\SKILL.md"
        Target = ".codex\skills\paper-spine-rewrite\SKILL.md"
    },
    @{
        Source = "skills\paper-spine-rewrite\references\rewrite-matrix.md"
        Target = ".codex\skills\paper-spine-rewrite\references\rewrite-matrix.md"
    },
    @{
        Source = "skills\paper-spine-audit\SKILL.md"
        Target = ".codex\skills\paper-spine-audit\SKILL.md"
    },
    @{
        Source = "skills\paper-spine-latex\SKILL.md"
        Target = ".codex\skills\paper-spine-latex\SKILL.md"
    },
    @{
        Source = "skills\paper-spine-research\references\style-learning-workflow.md"
        Target = ".codex\skills\paper-spine-research\references\style-learning-workflow.md"
    },
    @{
        Source = "skills\paper-spine-update\scripts\paperspine_update.py"
        Target = ".codex\skills\paper-spine-update\scripts\paperspine_update.py"
    },
    @{
        Source = "skills\nature-writing\SKILL.md"
        Target = ".codex\skills\nature-writing\SKILL.md"
    },
    @{
        Source = "skills\nature-polishing\static\core\hydraulic-engineering.md"
        Target = ".codex\skills\nature-polishing\static\core\hydraulic-engineering.md"
    },
    @{
        Source = "skills\nature-polishing\SKILL.md"
        Target = ".codex\skills\nature-polishing\SKILL.md"
    },
    @{
        Source = "skills\docx-editor-cn\SKILL.md"
        Target = ".codex\skills\docx-editor-cn\SKILL.md"
    },
    @{
        Source = "skills\docx-editor-cn\scripts\apply_format_contract.py"
        Target = ".codex\skills\docx-editor-cn\scripts\apply_format_contract.py"
    },
    @{
        Source = "skills\docx-editor-cn\scripts\format_contract_guard.py"
        Target = ".codex\skills\docx-editor-cn\scripts\format_contract_guard.py"
    },
    @{
        Source = "skills\docx-editor-cn\scripts\word_structure_guard.py"
        Target = ".codex\skills\docx-editor-cn\scripts\word_structure_guard.py"
    }
)

Write-Host "Installing Hydro Writing Core skill extensions..."
Write-Host "Codex skills directory: $CodexSkills"

foreach ($Map in $Mappings) {
    $Source = Join-Path $RepoRoot $Map.Source
    $Target = Join-Path $HOME $Map.Target
    $TargetDir = Split-Path -Parent $Target

    if (-not (Test-Path -LiteralPath $Source)) {
        throw "Missing source file: $Source"
    }

    New-Item -ItemType Directory -Force -Path $TargetDir | Out-Null

    if ((Test-Path -LiteralPath $Target) -and $Backup -and (-not $NoBackup)) {
        $BackupPath = "$Target.bak-$Stamp"
        Copy-Item -LiteralPath $Target -Destination $BackupPath -Force
        Write-Host "Backed up: $BackupPath"
    }

    Copy-Item -LiteralPath $Source -Destination $Target -Force
    Write-Host "Installed: $Target"
}

$BadFound = $false
foreach ($Map in $Mappings) {
    $Target = Join-Path $HOME $Map.Target
    $Text = Get-Content -LiteralPath $Target -Raw -Encoding UTF8
    $HasMojibake = $Text.Contains([char]0x9356) -or $Text.Contains([char]0x7ed7)
    $HasReplacementChar = $Text.Contains([char]0xFFFD)
    if ($HasMojibake -or $HasReplacementChar) {
        Write-Warning "Possible mojibake found in: $Target"
        $BadFound = $true
    }
}

if ($BadFound) {
    throw "Install finished, but encoding validation found suspicious characters."
}

Write-Host "Install finished. Restart Codex or open a new thread if the updated skills are not picked up immediately."
