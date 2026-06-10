param(
    [string]$TargetRoot,
    [switch]$DryRun,
    [switch]$NoBackup,
    [switch]$Backup
)

$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$InstallRoot = if ([string]::IsNullOrWhiteSpace($TargetRoot)) { $HOME } else { $TargetRoot }
$InstallRoot = [System.IO.Path]::GetFullPath($InstallRoot)
$CodexSkills = Join-Path $InstallRoot ".codex\skills"
$Stamp = Get-Date -Format "yyyyMMdd-HHmmss"
$ShouldBackup = $true

if ($NoBackup) {
    $ShouldBackup = $false
}

function Write-Utf8NoBomIfChanged {
    param(
        [string]$Path,
        [string]$Text,
        [string]$Message,
        [switch]$DryRun
    )

    if (-not (Test-Path -LiteralPath $Path)) {
        return
    }

    $Current = Get-Content -LiteralPath $Path -Raw -Encoding UTF8
    if ($Current -ne $Text) {
        if ($DryRun) {
            Write-Host "[DryRun] Would update: $Path"
            return
        }
        $Encoding = [System.Text.UTF8Encoding]::new($false)
        [System.IO.File]::WriteAllText($Path, $Text, $Encoding)
        Write-Host $Message
    }
}

function Remove-HydroNatureOverlay {
    param(
        [string]$Root,
        [switch]$DryRun
    )

    $WritingSkill = Join-Path $Root ".codex\skills\nature-writing\SKILL.md"
    $PolishingSkill = Join-Path $Root ".codex\skills\nature-polishing\SKILL.md"
    $PolishingManifest = Join-Path $Root ".codex\skills\nature-polishing\manifest.yaml"

    if (Test-Path -LiteralPath $WritingSkill) {
        $Text = Get-Content -LiteralPath $WritingSkill -Raw -Encoding UTF8
        $Text = $Text.Replace(" For water-conservancy, hydrology, hydraulic engineering, water resources, river, drainage, urban flooding, and water-environment topics, use the hydraulic-engineering core as the domain guardrail.", "")
        $Text = [regex]::Replace($Text, "(?s) For water-related papers,.*?chapter duties are confirmed\.", "")
        $Text = [regex]::Replace($Text, "(?s)\r?\nIf the request is for a Chinese report, course report, course design, course.*?do not copy text or import unsupported claims\.\r?\n", "`r`n")
        Write-Utf8NoBomIfChanged -Path $WritingSkill -Text $Text -Message "Cleaned old hydro overlay from Nature writing entrypoint." -DryRun:$DryRun
    }

    if (Test-Path -LiteralPath $PolishingSkill) {
        $Text = Get-Content -LiteralPath $PolishingSkill -Raw -Encoding UTF8
        $Text = [regex]::Replace($Text, ", and on Chinese reports, course reports, course designs, course papers, engineering reports, .*? water/hydraulic academic or coursework prose\. For water-conservancy topics, use the hydraulic-engineering core directly\.", ".")
        $Text = [regex]::Replace($Text, "(?s) For water-related papers,.*?after content is stable\.", "")
        $Text = [regex]::Replace($Text, "(?s)\r?\nIf the request is for a Chinese report, course report, course design, course.*?do not copy text or import unsupported claims\.\r?\n", "`r`n")
        Write-Utf8NoBomIfChanged -Path $PolishingSkill -Text $Text -Message "Cleaned old hydro overlay from Nature polishing entrypoint." -DryRun:$DryRun
    }

    if (Test-Path -LiteralPath $PolishingManifest) {
        $Text = Get-Content -LiteralPath $PolishingManifest -Raw -Encoding UTF8
        $Text = [regex]::Replace($Text, "(?m)^\s+- static/core/hydraulic-engineering\.md\r?\n", "")
        Write-Utf8NoBomIfChanged -Path $PolishingManifest -Text $Text -Message "Removed hydro core from Nature polishing always_load." -DryRun:$DryRun
    }
}

$RequiredExisting = @(
    ".codex\skills\paper-spine\SKILL.md",
    ".codex\skills\paper-spine-latex\SKILL.md",
    ".codex\skills\nature-writing\manifest.yaml",
    ".codex\skills\nature-polishing\manifest.yaml"
)

foreach ($Required in $RequiredExisting) {
    $RequiredPath = Join-Path $InstallRoot $Required
    if (-not (Test-Path -LiteralPath $RequiredPath)) {
        throw "Missing prerequisite: $RequiredPath. Install the base PaperSpine/Nature skills before applying hydro-writing-core."
    }
}

$InheritedSupportFiles = @(
    ".codex\skills\paper-spine\scripts\integrity_audit.py",
    ".codex\skills\paper-spine\scripts\structured_review.py",
    ".codex\skills\paper-spine\scripts\artifact_check.py",
    ".codex\skills\paper-spine-ui\scripts\launch_paperspine_ui.ps1"
)

$MissingInherited = @()
foreach ($Inherited in $InheritedSupportFiles) {
    $InheritedPath = Join-Path $InstallRoot $Inherited
    if (-not (Test-Path -LiteralPath $InheritedPath)) {
        $MissingInherited += $InheritedPath
    }
}

if ($MissingInherited.Count -gt 0) {
    Write-Warning "Some inherited base-skill support files are missing. Hydro Writing Core can still install, but workflows that reference these files may fail until the base PaperSpine skills are repaired."
    foreach ($Path in $MissingInherited) {
        Write-Warning "Missing inherited support: $Path"
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
        Source = "skills\nature-polishing\static\core\hydraulic-engineering.md"
        Target = ".codex\skills\nature-polishing\static\core\hydraulic-engineering.md"
    }
)

if ($DryRun) {
    Write-Host "Dry run: no files will be copied or modified."
}
Write-Host "Installing Hydro Writing Core skill extensions..."
Write-Host "Install root: $InstallRoot"
Write-Host "Codex skills directory: $CodexSkills"
Write-Host "Backup existing active files: $ShouldBackup"

foreach ($Map in $Mappings) {
    $Source = Join-Path $RepoRoot $Map.Source
    $Target = Join-Path $InstallRoot $Map.Target
    $TargetDir = Split-Path -Parent $Target

    if (-not (Test-Path -LiteralPath $Source)) {
        throw "Missing source file: $Source"
    }

    if ($DryRun) {
        if (Test-Path -LiteralPath $Target) {
            if ($ShouldBackup) {
                Write-Host "[DryRun] Would back up: $Target"
            }
            Write-Host "[DryRun] Would overwrite: $Target"
        } else {
            Write-Host "[DryRun] Would install new file: $Target"
        }
        continue
    }

    New-Item -ItemType Directory -Force -Path $TargetDir | Out-Null

    if ((Test-Path -LiteralPath $Target) -and $ShouldBackup) {
        $BackupPath = "$Target.bak-$Stamp"
        Copy-Item -LiteralPath $Target -Destination $BackupPath -Force
        Write-Host "Backed up: $BackupPath"
    }

    Copy-Item -LiteralPath $Source -Destination $Target -Force
    Write-Host "Installed: $Target"
}

Remove-HydroNatureOverlay -Root $InstallRoot -DryRun:$DryRun

if ($DryRun) {
    Write-Host "Dry run finished. No validation was run because no files were modified."
    exit 0
}

$BadFound = $false
$ValidationTargets = @($Mappings | ForEach-Object { Join-Path $InstallRoot $_.Target })
$ValidationTargets += @(
    (Join-Path $InstallRoot ".codex\skills\nature-writing\SKILL.md"),
    (Join-Path $InstallRoot ".codex\skills\nature-polishing\SKILL.md"),
    (Join-Path $InstallRoot ".codex\skills\nature-polishing\manifest.yaml")
)
foreach ($Target in $ValidationTargets) {
    if (-not (Test-Path -LiteralPath $Target)) {
        continue
    }
    $Text = Get-Content -LiteralPath $Target -Raw -Encoding UTF8
    $CommonMojibakeFragments = @(
        [char]0x9286,
        [char]0x9428,
        [char]0x6d60,
        [char]0x59af,
        [char]0x7ecb,
        [char]0x59d8,
        [char]0x951b,
        [char]0x6d93,
        [char]0x9365
    )
    $HasMojibake = $false
    if ($null -ne $Text) {
        foreach ($Fragment in $CommonMojibakeFragments) {
            if ($Text.Contains($Fragment)) {
                $HasMojibake = $true
                break
            }
        }
    }
    $HasReplacementChar = ($null -ne $Text) -and $Text.Contains([char]0xFFFD)
    if ($HasMojibake -or $HasReplacementChar) {
        Write-Warning "Possible mojibake found in: $Target"
        $BadFound = $true
    }
}

if ($BadFound) {
    throw "Install finished, but encoding validation found suspicious characters."
}

Write-Host "Install finished. Restart Codex or open a new thread if the updated skills are not picked up immediately."
