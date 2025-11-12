# update_project_structure.py
"""
更新项目结构脚本
"""

import os
from pathlib import Path


def create_gui_structure():
    """创建GUI目录结构"""
    print("创建GUI目录结构...")

    # 创建GUI目录
    gui_dir = Path('src/gui')
    gui_dir.mkdir(exist_ok=True)

    # 创建组件目录
    components_dir = gui_dir / 'components'
    components_dir.mkdir(exist_ok=True)

    # 创建样式目录
    styles_dir = gui_dir / 'styles'
    styles_dir.mkdir(exist_ok=True)

    # 创建必要的空文件
    files_to_create = [
        'src/gui/__init__.py',
        'src/gui/components/__init__.py',
        'src/gui/styles/__init__.py'
    ]

    for file_path in files_to_create:
        Path(file_path).touch()
        print(f"创建文件: {file_path}")

    print("✅ GUI目录结构创建完成")


def main():
    """主函数"""
    print("=" * 50)
    print("更新ADM1项目结构")
    print("=" * 50)

    create_gui_structure()

    print("\n新文件需要手动创建:")
    print("1. adm1_gui.py - GUI启动器")
    print("2. src/gui/main_window.py - 主窗口")
    print("3. test_gui.py - 测试脚本")

    print("\n请将上述代码复制到对应文件中")


if __name__ == "__main__":
    main()