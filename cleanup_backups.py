# cleanup_backups.py
"""
一键清理备份文件
删除所有冗余备份，保留核心功能
"""

import os
import shutil
from pathlib import Path


def cleanup_backups():
    """清理所有备份文件"""
    print("=" * 50)
    print("ADM1项目备份清理工具")
    print("=" * 50)

    # 要删除的备份目录列表
    backup_dirs = [
        "backup_before_fix",
        "project_backup_complete",
        "project_restructure_backup"
    ]

    # 要删除的备份文件模式
    backup_patterns = [
        "*.backup",
        "*.bak",
        "*.old",
        "*~"
    ]

    # 特定要删除的备份文件
    specific_files = [
        "src/main_fixed.py",
        "src/visualization/plot_manager.py.backup",
        "src/visualization/result_visualizer.py.backup"
    ]

    deleted_count = 0

    # 1. 删除备份目录
    print("删除备份目录:")
    for dir_name in backup_dirs:
        dir_path = Path(dir_name)
        if dir_path.exists():
            try:
                shutil.rmtree(dir_path)
                print(f"  [DELETED] 目录: {dir_name}")
                deleted_count += 1
            except Exception as e:
                print(f"  [ERROR] 删除失败 {dir_name}: {e}")

    # 2. 删除特定备份文件
    print("\n删除特定备份文件:")
    for file_path in specific_files:
        path = Path(file_path)
        if path.exists():
            try:
                path.unlink()
                print(f"  [DELETED] 文件: {file_path}")
                deleted_count += 1
            except Exception as e:
                print(f"  [ERROR] 删除失败 {file_path}: {e}")

    # 3. 删除所有匹配的备份文件
    print("\n删除匹配的备份文件:")
    for pattern in backup_patterns:
        for file_path in Path('.').rglob(pattern):
            try:
                file_path.unlink()
                print(f"  [DELETED] 文件: {file_path}")
                deleted_count += 1
            except Exception as e:
                print(f"  [ERROR] 删除失败 {file_path}: {e}")

    # 4. 清理空目录
    print("\n清理空目录:")
    for dir_path in Path('.').rglob('*'):
        if dir_path.is_dir() and not any(dir_path.iterdir()):
            try:
                dir_path.rmdir()
                print(f"  [DELETED] 空目录: {dir_path}")
                deleted_count += 1
            except:
                pass

    print("\n" + "=" * 50)
    print(f"清理完成: 共删除 {deleted_count} 个项目")
    print("=" * 50)


def preview_cleanup():
    """预览将要删除的文件（不实际删除）"""
    print("=" * 50)
    print("清理预览（不实际删除）")
    print("=" * 50)

    backup_dirs = [
        "backup_before_fix",
        "project_backup_complete",
        "project_restructure_backup"
    ]

    backup_patterns = [
        "*.backup",
        "*.bak",
        "*.old",
        "*~"
    ]

    specific_files = [
        "src/main_fixed.py",
        "src/visualization/plot_manager.py.backup",
        "src/visualization/result_visualizer.py.backup"
    ]

    total_count = 0

    print("将要删除的目录:")
    for dir_name in backup_dirs:
        dir_path = Path(dir_name)
        if dir_path.exists():
            file_count = len(list(dir_path.rglob('*')))
            print(f"  [DIR] {dir_name} ({file_count} 个文件)")
            total_count += file_count

    print("\n将要删除的特定文件:")
    for file_path in specific_files:
        path = Path(file_path)
        if path.exists():
            print(f"  [FILE] {file_path}")
            total_count += 1

    print("\n将要删除的匹配文件:")
    for pattern in backup_patterns:
        files = list(Path('.').rglob(pattern))
        for file_path in files:
            print(f"  [FILE] {file_path}")
            total_count += 1

    print("\n" + "=" * 50)
    print(f"总计: {total_count} 个文件/目录将被删除")
    print("=" * 50)

    return total_count


def main():
    """主函数"""
    print("选择操作:")
    print("1. 预览将要删除的内容")
    print("2. 执行清理")
    print("3. 退出")

    choice = input("请输入选择 (1/2/3): ").strip()

    if choice == "1":
        preview_cleanup()
    elif choice == "2":
        # 先预览
        total = preview_cleanup()
        if total > 0:
            confirm = input(f"确认删除 {total} 个文件/目录? (y/N): ").strip().lower()
            if confirm == 'y':
                cleanup_backups()
            else:
                print("取消清理")
        else:
            print("没有找到需要清理的文件")
    else:
        print("退出")


if __name__ == "__main__":
    main()