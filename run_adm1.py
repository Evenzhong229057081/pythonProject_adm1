# run_adm1.py
"""
智能启动器 - 自动选择最佳运行方式
"""

import subprocess
import sys
from pathlib import Path


def detect_best_runner():
    """检测最佳运行方式"""
    # 尝试标准导入
    try:
        src_path = Path('src')
        if str(src_path) not in sys.path:
            sys.path.insert(0, str(src_path))

        from interface.cli_interface import main
        return "standard"  # 标准版本可用
    except:
        pass

    # 尝试安全导入
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "test", Path('src/core/adm1_model.py')
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return "fixed"  # 修复版本可用
    except:
        pass

    return "unknown"  # 都不可用


def main():
    """智能启动"""
    print("ADM1智能启动器")
    print("检测最佳运行方式...")

    mode = detect_best_runner()

    if mode == "standard":
        print("✅ 使用标准版本")
        subprocess.run([sys.executable, "src/main.py"])
    elif mode == "fixed":
        print("🔧 使用修复版本")
        subprocess.run([sys.executable, "src/main_fixed.py"])
    else:
        print("❌ 无法确定运行方式")
        print("请手动运行:")
        print("  python src/main.py      # 标准版本")
        print("  python src/main_fixed.py # 修复版本")


if __name__ == "__main__":
    main()