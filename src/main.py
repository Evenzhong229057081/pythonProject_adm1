# src/main.py（确保支持return_results参数）
"""
ADM1主程序 - 支持GUI调用
"""

import sys
from pathlib import Path


def main(return_results=False):
    """主程序入口 - 支持GUI调用"""
    print("=" * 60)
    print("ADM1厌氧消化模型系统")
    print("=" * 60)

    # 设置环境
    src_path = Path(__file__).parent
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))

    Path('results').mkdir(exist_ok=True)
    Path('figures').mkdir(exist_ok=True)

    print(f"Python版本: {sys.version.split()[0]}")
    print(f"工作目录: {Path.cwd()}")
    print(f"输出目录: results/, figures/")

    # 优先尝试补丁模式
    try:
        from patches.environment_patch import apply_patch_and_run
        print("使用补丁模式运行")

        if return_results:
            # GUI模式：返回结果
            return apply_patch_and_run(return_results=True)
        else:
            # 命令行模式：直接运行
            apply_patch_and_run()
            return None

    except Exception as e:
        print(f"补丁模式失败: {e}")
        if return_results:
            return {'success': False, 'message': f'补丁模式失败: {e}'}

    # 备用标准模式
    try:
        from interface.cli_interface import main as interface_main
        print("使用标准模式运行")

        if return_results:
            # GUI模式：需要适配interface_main支持return_results
            return {'success': False, 'message': '标准模式不支持GUI调用'}
        else:
            interface_main()
            return None

    except Exception as e:
        print(f"标准模式失败: {e}")
        if return_results:
            return {'success': False, 'message': f'标准模式失败: {e}'}

    error_msg = "所有模式均失败，请检查环境配置"
    print(error_msg)
    if return_results:
        return {'success': False, 'message': error_msg}


if __name__ == "__main__":
    # 命令行模式：不传递参数
    main()