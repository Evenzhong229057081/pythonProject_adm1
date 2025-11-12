# test_environment.py - 环境验证脚本
import sys


def check_environment():
    """检查Python环境是否满足ADM1开发需求"""
    required_packages = {
        'numpy': '1.21.0',
        'scipy': '1.7.0',
        'pandas': '1.3.0',
        'matplotlib': '3.5.0'
    }

    print("=== ADM1开发环境验证 ===")
    all_ok = True

    # 检查Python版本
    py_version = sys.version_info
    print(f"Python版本: {py_version.major}.{py_version.minor}.{py_version.micro}")
    if py_version < (3, 8):
        print("⚠ 警告: 建议使用Python 3.8+版本")
        all_ok = False

    # 检查关键包
    for pkg, req_ver in required_packages.items():
        try:
            import importlib
            module = importlib.import_module(pkg)
            current_ver = getattr(module, '__version__', '未知')
            print(f"✅ {pkg:>10}: 已安装 (版本: {current_ver})")
        except ImportError:
            print(f"❌ {pkg:>10}: 未安装 (需要版本: {req_ver}+)")
            all_ok = False

    if all_ok:
        print("\n环境验证通过！可以开始ADM1开发")
    else:
        print("\n环境不完整，请先安装缺失的包")


if __name__ == "__main__":
    check_environment()