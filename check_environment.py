# check_environment.py
"""
环境检测工具 - 专业无emoji版本
"""

import sys
from pathlib import Path


def check_standard_import():
    """检查标准导入"""
    print("[PROGRESS] 检查标准导入模式")
    try:
        src_path = Path('src')
        if str(src_path) not in sys.path:
            sys.path.insert(0, str(src_path))

        from interface.cli_interface import main
        print("[SUCCESS] 标准导入模式可用")
        return True
    except Exception as e:
        print(f"[ERROR] 标准导入模式失败: {e}")
        return False


def check_safe_import():
    """检查安全导入"""
    print("[PROGRESS] 检查安全导入模式")
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "test", Path('src/core/adm1_model.py')
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        print("[SUCCESS] 安全导入模式可用")
        return True
    except Exception as e:
        print(f"[ERROR] 安全导入模式失败: {e}")
        return False


def main():
    """主检测函数"""
    print("=" * 50)
    print("ADM1环境检测工具")
    print("=" * 50)

    # 检查导入模式
    std_ok = check_standard_import()
    safe_ok = check_safe_import()

    print("\n" + "=" * 50)
    print("检测结果汇总")
    print("=" * 50)

    if std_ok:
        print("[SUCCESS] 推荐使用标准模式")
        print("运行命令: python src/main.py")
    elif safe_ok:
        print("[SUCCESS] 推荐使用补丁模式")
        print("运行命令: python src/main.py")
    else:
        print("[ERROR] 无可用运行模式")
        print("[INFO] 请检查环境配置和文件完整性")


if __name__ == "__main__":
    main()