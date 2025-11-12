# check_gui_import.py
"""
GUI导入诊断工具
"""

import sys
from pathlib import Path


def check_gui_import():
    """检查GUI导入问题"""
    print("=" * 60)
    print("GUI导入诊断")
    print("=" * 60)

    # 添加src到路径
    project_root = Path(__file__).parent
    src_path = project_root / 'src'
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))
        print(f"✅ 已添加路径: {src_path}")

    # 检查文件是否存在
    gui_files = [
        src_path / 'gui' / '__init__.py',
        src_path / 'gui' / 'main_window.py'
    ]

    for file_path in gui_files:
        if file_path.exists():
            print(f"✅ 文件存在: {file_path}")
        else:
            print(f"❌ 文件不存在: {file_path}")
            return False

    # 测试导入
    try:
        from gui import ADM1MainWindow
        print("✅ GUI模块导入成功")
        return True
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 其他错误: {e}")
        return False


if __name__ == "__main__":
    if check_gui_import():
        print("\n🎉 诊断通过！可以运行GUI")
        print("运行命令: python adm1_gui.py")
    else:
        print("\n💡 请检查文件结构和__init__.py文件内容")