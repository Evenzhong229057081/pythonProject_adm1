# debug_detailed.py（修复版）
"""
详细错误定位调试 - 修复Mock对象问题
"""

import sys
from pathlib import Path
import tkinter as tk
from tkinter import ttk
import traceback


def detailed_debug():
    """详细调试 - 使用真实的Tkinter对象"""
    src_path = Path('src')
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))

    # 创建真实的Tkinter环境
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口

    try:
        print("=" * 60)
        print("详细错误定位调试")
        print("=" * 60)

        # 创建真实的notebook控件
        notebook = ttk.Notebook(root)

        print("✅ Tkinter环境初始化成功")

        # 测试模拟标签页
        from gui.components.simulation_tab import SimulationTab

        print("✅ 模拟标签页导入成功")

        # 创建测试窗口对象
        class TestWindow:
            def __init__(self, notebook):
                self.notebook = notebook
                self.root = root

        test_window = TestWindow(notebook)

        # 测试实例化
        tab = SimulationTab(test_window)
        print("✅ 模拟标签页实例化成功")

        # 测试模拟运行
        print("\n测试模拟运行...")
        try:
            results = tab._run_real_simulation()
            print("✅ 模拟运行成功")

            # 检查结果有效性
            if results and isinstance(results, dict):
                print(f"结果类型: {type(results)}")
                print(f"包含键: {list(results.keys())}")

                # 检查success字段
                success = results.get('success')
                print(f"success值: {success} (类型: {type(success)})")

                # 测试布尔判断
                print("\n测试布尔判断方法:")
                test_methods = [
                    ('直接bool', lambda: bool(success)),
                    ('if语句', lambda: True if success else False),
                    ('逻辑与', lambda: success and True),
                    ('逻辑或', lambda: success or False)
                ]

                for name, test_func in test_methods:
                    try:
                        result = test_func()
                        print(f"✅ {name}: {result}")
                    except Exception as e:
                        print(f"❌ {name}失败: {e}")
                        traceback.print_exc()

                return True
            else:
                print("❌ 模拟返回无效结果")
                return False

        except Exception as e:
            print(f"❌ 模拟测试失败: {e}")
            traceback.print_exc()
            return False

    except Exception as e:
        print(f"❌ 调试失败: {e}")
        traceback.print_exc()
        return False
    finally:
        root.destroy()  # 清理资源


if __name__ == "__main__":
    detailed_debug()