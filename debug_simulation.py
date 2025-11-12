# debug_simulation.py
"""
调试脚本 - 诊断模拟问题
"""

import sys
from pathlib import Path


def debug_simulation():
    """调试模拟过程"""
    src_path = Path('src')
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))

    try:
        from patches.environment_patch import apply_patch

        print("开始调试模拟...")
        results = apply_patch(return_results=True)

        print("模拟结果类型:", type(results))
        print("结果键:", list(results.keys()) if isinstance(results, dict) else "不是字典")

        if isinstance(results, dict):
            for key, value in results.items():
                if key == 'success':
                    print(f"success 类型: {type(value)}")
                    print(f"success 值: {value}")
                    if hasattr(value, '__len__'):
                        print(f"success 长度: {len(value)}")
                    if hasattr(value, 'shape'):
                        print(f"success 形状: {value.shape}")
                elif key == 'states':
                    if hasattr(value, 'shape'):
                        print(f"states 形状: {value.shape}")
                elif key == 'time':
                    print(f"time 长度: {len(value)}")

        return results

    except Exception as e:
        print(f"调试失败: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    debug_simulation()