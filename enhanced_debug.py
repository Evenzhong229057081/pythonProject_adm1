# enhanced_debug.py
"""
增强调试脚本 - 定位具体错误位置
"""

import sys
from pathlib import Path
import traceback


def enhanced_debug():
    """增强调试"""
    src_path = Path('src')
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))

    try:
        print("=" * 50)
        print("增强调试模式")
        print("=" * 50)

        # 测试直接调用
        from patches.environment_patch import apply_patch
        print("✅ apply_patch导入成功")

        results = apply_patch(return_results=True)
        print("✅ apply_patch调用成功")

        # 详细检查结果结构
        print("\n详细结果分析:")
        print("-" * 30)

        for key, value in results.items():
            print(f"{key}: {type(value)} -> {repr(value)[:100]}...")

        # 测试布尔判断
        print("\n布尔判断测试:")
        print("-" * 20)

        success = results.get('success')
        print(f"success类型: {type(success)}")
        print(f"success值: {success}")

        # 各种布尔判断方式测试
        try:
            test1 = bool(success)
            print(f"bool(success): {test1} ✅")
        except Exception as e:
            print(f"bool(success)失败: {e} ❌")

        try:
            if hasattr(success, 'any'):
                test2 = bool(success.any())
                print(f"success.any(): {test2} ✅")
        except Exception as e:
            print(f"success.any()失败: {e} ❌")

        return results

    except Exception as e:
        print(f"❌ 调试失败: {e}")
        traceback.print_exc()
        return None


if __name__ == "__main__":
    enhanced_debug()