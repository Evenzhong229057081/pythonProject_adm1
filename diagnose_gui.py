# diagnose_gui.py
"""
GUI诊断脚本 - 检查文件结构和导入问题
"""

import sys
import os
from pathlib import Path


def check_file_structure():
    """检查文件结构"""
    print("=" * 60)
    print("GUI文件结构诊断")
    print("=" * 60)

    base_path = Path('src/gui')

    # 检查必要目录和文件
    required_structure = {
        base_path: ['__init__.py'],
        base_path / 'components': ['__init__.py', 'charts_tab.py', 'help_tab.py', 'parameters_tab.py',
                                   'simulation_tab.py'],
        base_path / 'utils': ['__init__.py', 'chart_manager.py'],
        base_path / 'widgets': ['__init__.py', 'main_window.py', 'chart_integration.py']
    }

    all_ok = True
    for directory, files in required_structure.items():
        if not directory.exists():
            print(f"❌ 目录不存在: {directory}")
            all_ok = False
            continue

        for file in files:
            file_path = directory / file
            if not file_path.exists():
                print(f"❌ 文件不存在: {file_path}")
                all_ok = False
            else:
                # 检查文件是否为空
                if file_path.stat().st_size == 0:
                    print(f"⚠️  文件为空: {file_path}")
                else:
                    print(f"✅ 文件正常: {file_path}")

    return all_ok


def check_init_file_contents():
    """检查__init__.py文件内容"""
    print("\n" + "=" * 60)
    print("检查__init__.py文件内容")
    print("=" * 60)

    init_files = [
        'src/gui/__init__.py',
        'src/gui/components/__init__.py',
        'src/gui/utils/__init__.py',
        'src/gui/widgets/__init__.py'
    ]

    for file_path in init_files:
        path = Path(file_path)
        if path.exists():
            content = path.read_text(encoding='utf-8').strip()
            if not content:
                print(f"❌ {file_path} 是空文件")
            elif 'from' not in content and 'import' not in content:
                print(f"⚠️  {file_path} 缺少导入语句")
            else:
                print(f"✅ {file_path} 内容正常")
        else:
            print(f"❌ {file_path} 不存在")


def check_python_path():
    """检查Python路径"""
    print("\n" + "=" * 60)
    print("检查Python路径")
    print("=" * 60)

    src_path = Path('src')
    if str(src_path) not in sys.path:
        print("❌ src目录不在Python路径中")
        print("当前Python路径:")
        for path in sys.path:
            print(f"  {path}")
        return False
    else:
        print("✅ src目录在Python路径中")
        return True


def test_imports():
    """测试模块导入"""
    print("\n" + "=" * 60)
    print("测试模块导入")
    print("=" * 60)

    # 确保src在路径中
    src_path = Path('src')
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))

    try:
        # 测试导入主模块
        from gui import ADM1MainWindow
        print("✅ gui模块导入成功")

        # 测试导入组件
        from gui.components import ChartsTab, HelpTab, ParametersTab, SimulationTab
        print("✅ 组件模块导入成功")

        # 测试导入工具
        from gui.utils import ChartManager
        print("✅ 工具模块导入成功")

        # 测试导入小部件
        from gui.widgets import ADM1MainWindow as WidgetMainWindow
        print("✅ 小部件模块导入成功")

        return True

    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    except Exception as e:
        print(f"❌ 其他错误: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主诊断函数"""
    print("开始诊断GUI启动问题...\n")

    checks = [
        ("文件结构检查", check_file_structure),
        ("初始化文件检查", check_init_file_contents),
        ("Python路径检查", check_python_path),
        ("模块导入测试", test_imports)
    ]

    results = []
    for check_name, check_func in checks:
        print(f"\n执行: {check_name}")
        result = check_func()
        results.append((check_name, result))

    print("\n" + "=" * 60)
    print("诊断结果汇总")
    print("=" * 60)

    all_passed = True
    for check_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{check_name}: {status}")
        if not result:
            all_passed = False

    if all_passed:
        print("\n🎉 所有检查通过！GUI应该可以正常运行")
        print("运行命令: python adm1_gui.py")
    else:
        print("\n💡 请根据上面的错误信息修复问题")

    return all_passed


if __name__ == "__main__":
    main()