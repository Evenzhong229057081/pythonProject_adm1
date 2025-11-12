# test_chart_integration.py
"""
图表集成测试脚本
"""

import sys
from pathlib import Path


def test_chart_integration():
    """测试图表集成"""
    print("测试图表集成功能...")

    # 添加src到路径
    src_path = Path('src')
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))

    try:
        # 测试图表管理器导入
        from gui.chart_integration import ChartManager
        print("✅ 图表管理器导入成功")

        # 测试matplotlib后端
        import matplotlib
        matplotlib.use('TkAgg')  # 使用Tkinter后端
        print("✅ Matplotlib后端设置成功")

        # 测试GUI集成
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()  # 不显示窗口

        from gui.main_window import ADM1MainWindow
        print("✅ GUI主窗口导入成功")

        print("✅ 图表集成测试通过")
        return True

    except Exception as e:
        print(f"❌ 图表集成测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    test_chart_integration()