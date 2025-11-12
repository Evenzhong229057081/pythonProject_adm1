# cleanup.ps1
# ADM1项目一键清理脚本

Write-Host "================================================"
Write-Host "ADM1项目备份清理工具"
Write-Host "================================================"

# 备份目录列表
$BackupDirs = @(
    "backup_before_fix",
    "project_backup_complete",
    "project_restructure_backup"
)

# 备份文件模式
$BackupPatterns = @("*.backup", "*.bak", "*.old", "*~")

# 特定备份文件
$SpecificFiles = @(
    "src\main_fixed.py",
    "src\visualization\plot_manager.py.backup",
    "src\visualization\result_visualizer.py.backup"
)

$DeletedCount = 0

# 删除备份目录
Write-Host "删除备份目录:"
foreach ($Dir in $BackupDirs) {
    if (Test-Path $Dir) {
        try {
            Remove-Item -Recurse -Force $Dir
            Write-Host "  [DELETED] 目录: $Dir"
            $DeletedCount++
        } catch {
            Write-Host "  [ERROR] 删除失败 $Dir : $_"
        }
    }
}

# 删除特定文件
Write-Host "`n删除特定备份文件:"
foreach ($File in $SpecificFiles) {
    if (Test-Path $File) {
        try {
            Remove-Item -Force $File
            Write-Host "  [DELETED] 文件: $File"
            $DeletedCount++
        } catch {
            Write-Host "  [ERROR] 删除失败 $File : $_"
        }
    }
}

# 删除匹配文件
Write-Host "`n删除匹配的备份文件:"
foreach ($Pattern in $BackupPatterns) {
    $Files = Get-ChildItem -Recurse -Include $Pattern
    foreach ($File in $Files) {
        try {
            Remove-Item -Force $File.FullName
            Write-Host "  [DELETED] 文件: $($File.FullName)"
            $DeletedCount++
        } catch {
            Write-Host "  [ERROR] 删除失败 $($File.FullName) : $_"
        }
    }
}

Write-Host "`n================================================"
Write-Host "清理完成: 共删除 $DeletedCount 个项目"
Write-Host "================================================"